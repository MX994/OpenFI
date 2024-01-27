from flask import Flask, request, jsonify, render_template
from pathlib import Path
from api.devices import Devices
from api.devices.XYPlane import PositionMode
import json
import time
from threading import Lock, Thread
import importlib
from util import HarnessWrapper
from api.Harness import Harness
from numpy import arange

g_App = Flask(__name__)
g_Harness : HarnessWrapper = HarnessWrapper()
g_HarnessPath : Path = Path("harnesses")
g_JobPath = Path("jobs")
g_Devices = Devices()
g_Lock = Lock()
g_GlitchThread : Thread = None

@g_App.before_first_request
def initalize_io():
    # Initialize devices.
    g_Devices.Init()

@g_App.route("/")
def render_index():
    return render_template("attack_configuration.html")

@g_App.route("/attacks")
def render_attack_stats():
    return render_template("attack_stats.html")

'''
    API stuff
'''
@g_App.route("/api/glitch_types")
def get_glitch_types():
    return ["Crowbar", "Electromagnetic"]

@g_App.route("/api/harnesses")
def get_harnesses():
    return [x.stem for x in g_HarnessPath.glob("*") if x.is_dir()]

'''
    XYZ-Plane Routes
'''
@g_App.route("/api/xyz-plane/move", methods = ['POST'])
def set_xyz_position():
    data = dict(request.get_json())
    missing_keys = get_missing_parameters(['x', 'y', 'z', 'mode', 'speed'], data)
    if len(missing_keys) != 0:
        return {
            'kind' : 'error',
            'error': f'Need to specify the following keys: {missing_keys}.'
        }

    # Get parameters in right format.
    coordinates = (data['x'], data['y'], data['z'])
    speed = data['speed']
    match data['mode']:
        case 'absolute':
            position_mode = PositionMode.Absolute
        case 'relative':
            position_mode = PositionMode.Relative
        case '_':
            return {
                'kind' : 'error',
                'error': f'Unknown permission mode {data["mode"]}.'
            }
    # Do movement.
    g_Devices.XY.set_position_mode(position_mode)
    g_Devices.XY.move(coordinates, speed)

    # Return the new position.
    projected_position = g_Devices.XY.get_projected_position()
    result = {
        'kind' : 'success',
        'x': projected_position[0],
        'y': projected_position[1],
        'z': projected_position[2],
    }
    return jsonify(result)
    
@g_App.route("/api/xyz-plane/home", methods = ['POST'])
def home_xyz():
    # Home the XYZ Plane.
    g_Devices.XY.auto_home()

    # Return the new position.
    projected_position = g_Devices.XY.get_projected_position()
    result = {
        'kind' : 'success',
        'x': projected_position[0],
        'y': projected_position[1],
        'z': projected_position[2],
    }
    return jsonify(result)

@g_App.route("/api/xyz-plane/set-message", methods = ['GET'])
def set_xyz_message():
    data = dict(request.args)
    missing_keys = get_missing_parameters(['message'], data)

    if len(missing_keys) != 0:
        return {
            'kind' : 'error',
            'error': f'Need to specify the following keys: {missing_keys}.'
        }

    # Home the XYZ Plane.
    g_Devices.XY.set_message(data['message'])
    result = {
        'kind' : 'success',
    }
    return jsonify(result)

@g_App.route("/api/xyz-plane/get-coordinates", methods = ['GET'])
def get_current_coordinates():
    projected_position = g_Devices.XY.get_projected_position()
    result = {
        'kind' : 'success',
        'x': projected_position[0],
        'y': projected_position[1],
        'z': projected_position[2],
    }
    return jsonify(result)

'''
    EMP Routes
'''
@g_App.route("/api/emp/arm", methods = ['POST'])
def arm_emp():
    g_Devices.PicoEMP.arm()
    result = {
        'kind' : 'success',
    }
    return jsonify(result)

@g_App.route("/api/emp/disarm", methods = ['POST'])
def disarm_emp():
    g_Devices.PicoEMP.disarm()
    result = {
        'kind' : 'success',
    }
    return jsonify(result)

@g_App.route("/api/emp/fire", methods = ['POST'])
def pulse_emp():
    g_Devices.PicoEMP.pulse()
    result = {
        'kind' : 'success',
    }
    return jsonify(result)

'''
    Job API
'''
@g_App.route("/api/jobs/get", methods = ['GET'])
def get_job_list():
    result = {
        'kind' : 'success',
        'jobs' : []
    }
    for job in g_JobPath.glob('*.json'):
        with job.open('r') as job_data:
            result['jobs'].append(json.load(job_data))
    return jsonify(result)

@g_App.route("/api/jobs/start", methods = ['POST'])
def start_job():
    data = dict(request.get_json())
    with g_Lock:
        load_harness(data['harness'])
        g_GlitchThread = Thread(target=glitch_loop, args=(data,))
        g_GlitchThread.start()
    result = {
        'kind' : 'success',
    }
    return jsonify(result) 

# @g_App.route("/api/jobs/stop", methods = ['POST'])
# def stop_job():

#     return jsonify(result) 

def load_harness(name):
    harnesses = {}
    for harness_path in g_HarnessPath.glob("*"):
        if harness_path.is_dir():
            harnesses |= {
                harness_path.stem : harness_path
            }
    harness_path = harnesses[name]
    harness_spec = importlib.util.spec_from_file_location(name, (harness_path / 'harness.py').as_posix())
    harness_module = importlib.util.module_from_spec(harness_spec)
    harness_spec.loader.exec_module(harness_module)
    g_Harness.Set(harness_module.DeviceHarness(g_Devices))
    g_Harness.Get().configure()

def get_missing_parameters(expected, data : dict):
    # Check if we have the requested parameters.
    missing_keys = []
    for key in expected:
        if key not in data:
            missing_keys.append(key)
    return missing_keys

def glitch_loop(data):
    # Move gantry up and home printer.
    g_Devices.XY.set_position_mode(PositionMode.Relative)
    g_Devices.XY.move((0, 20, 0))
    g_Devices.XY.auto_home()
    g_Devices.XY.set_position_mode(PositionMode.Relative)
    g_Devices.XY.move((0, 50, 0))

    # Run the glitch iterations...
    while not g_Harness.Get().should_terminate():
        for x, y, z, ext_offset, repeat, tries in zip(
            arange(float(data['job_parameters']['x']['minimum']), float(data['job_parameters']['x']['maximum']), float(data['job_parameters']['x']['step'])),
            arange(float(data['job_parameters']['y']['minimum']), float(data['job_parameters']['y']['maximum']), float(data['job_parameters']['y']['step'])),
            arange(float(data['job_parameters']['z']['minimum']), float(data['job_parameters']['z']['maximum']), float(data['job_parameters']['z']['step'])),
            arange(float(data['job_parameters']['ext_offset']['minimum']), float(data['job_parameters']['ext_offset']['maximum']), float(data['job_parameters']['ext_offset']['step'])),
            arange(float(data['job_parameters']['repeat']['minimum']), float(data['job_parameters']['repeat']['maximum']), float(data['job_parameters']['repeat']['step'])),
            arange(float(data['job_parameters']['tries']['minimum']), float(data['job_parameters']['tries']['maximum']), float(data['job_parameters']['tries']['step'])),
        ):
            
            print(f'Position: ({x}, {y}, {z}) w/ Ext. Offset {ext_offset} and Repeat {repeat}')

            # If EMP XYZ Glitching Mode, move to the location                
            if data['job_type'] == 'emfi':
                g_Devices.XY.move((x, y, z))

            # Configure the GhettoGlitcher
            # g_Devices.GhettoGlitcher.set_ext_offset(ext_offset)
            # g_Devices.GhettoGlitcher.set_repeat(repeat)

            # Reset and test
            g_Harness.Get().reset()
            if g_Harness.Get().test():
                print('SUCCESS!')
                # self.glitchSuccess.emit((x, y, z, ext_offset, repeat))
            else:
                print('FAILURE!')