window.onload = () => {
  /* 
    Variables
  */
  let gantry_coordinates = ['x', 'y', 'z'].map(e => document.getElementById(`gantry-${e}-coordinate`));
  gantry_coordinates.forEach(e => {
    e.type = 'number';
  });

  let gantry_step = document.getElementById('gantry-step');
  gantry_step.type = 'number';
  gantry_step.onchange = () => {
    gantry_coordinates.forEach(e => {
      e.step = gantry_step.value;
    });
  };

  // Gantry controls.
  let gantry_forward_button = document.getElementById('gantry-move-forward-button');
  let gantry_backwards_button = document.getElementById('gantry-move-backwards-button');
  let gantry_left_button = document.getElementById('gantry-move-left-button');
  let gantry_right_button = document.getElementById('gantry-move-right-button');
  let gantry_up_button = document.getElementById('gantry-up-button');
  let gantry_down_button = document.getElementById('gantry-down-button');
  let gantry_home_button = document.getElementById('gantry-home-button');
  let gantry_commit_button = document.getElementById('gantry-commit-button');

  // EMP controls.
  let emp_arm_button = document.getElementById('emp-arm-button');
  let emp_disarm_button = document.getElementById('emp-disarm-button');
  let emp_fire_button = document.getElementById('emp-fire-button');

  // Harness dropdown targets.
  let harness_dropdown_button = document.getElementById('harness-button');
  let harness_selector = document.getElementById('harness-selector');
  let refresh_harness_button = document.getElementById('refresh-harness');

  // Other dropdown targets.
  let glitch_dropdown_button = document.getElementById('glitch-type-button');
  let glitch_types_selector = document.getElementById('glitch-type-selector');
  let refresh_glitch_button = document.getElementById('refresh-glitch-type');

  // Job Submitting
  let job_list_element = document.getElementById('job-history');
  let job_submit = document.getElementById('submit-attack-button');

  /* 
    Functions
  */
  async function build_parameter_table() {
    const parameters = ['X', 'Y', 'Z', 'Ext-Offset', 'Repeat', 'Tries'];
    const bounds = ['', 'Minimum', 'Maximum', 'Step'];
    const parameter_table = document.getElementById('parameter-list');

    // Build header row.
    let header = document.createElement('thead');
    let header_row = document.createElement('tr');
    bounds.forEach(e => {
      let header_element = document.createElement('th');
      header_element.scope = 'col';
      header_element.innerText = e;
      header_row.append(header_element);
    });
    header.append(header_row);
    parameter_table.append(header);

    // Build parameter rows.
    let body = document.createElement('tbody');
    parameters.forEach(e => {
      let body_row = document.createElement('tr');

      // Row header stuff.
      let row_header = document.createElement('th');
      row_header.scope = 'row';
      row_header.innerText = e;
      body_row.append(row_header);

      // Add new textboxes.
      bounds.slice(1).forEach(k => {
        let data = document.createElement('td');
        let input_control = document.createElement('input');
        input_control.type = 'number';
        input_control.step = '0.001';
        input_control.id = `${e}-${k}`
        input_control.value = 0;
        data.append(input_control);
        body_row.appendChild(data);
      });

      body.append(body_row);
    });
    parameter_table.append(body);
  }

  function update_coordinates(data) {
    gantry_coordinates[0].value = data['x'];
    gantry_coordinates[1].value = data['y'];
    gantry_coordinates[2].value = data['z'];
  }

  async function get_current_coordinates() {
    let result = await fetch(`/api/xyz-plane/get-coordinates`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    let result_json = await result.json();
    if (result_json['kind'] === 'success') {
      update_coordinates(result_json);
    }
  }

  async function move_emp(x, y, z, mode, speed) {
    let data = {
      x: x,
      y: y,
      z: z,
      mode: mode,
      speed: speed,
    };
    let result = await fetch(`/api/xyz-plane/move`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data)
    });
    let result_json = await result.json();
    if (result_json['kind'] === 'success') {
      update_coordinates(result_json);
    }
  }

  async function move_emp_relative(x, y, z, speed = 9600) {
    move_emp(x, y, z, 'relative', speed);
  }

  async function move_emp_absolute(x, y, z, speed = 9600) {
    move_emp(x, y, z, 'absolute', speed);
  }

  async function populate_job_history() {
    /*
      <div class="accordion-item">
        <h2 class="accordion-header">
          <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
            data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">
            Accordion Item #1
          </button>
        </h2>
        <div id="flush-collapseOne" class="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
          <div class="accordion-body">Placeholder content for this accordion, which is intended to demonstrate the
            <code>.accordion-flush</code> class. This is the first item's accordion body.
          </div>
        </div>
      </div>
    */
    const jobs = await (await fetch('/api/jobs/get', {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      }
    })).json();
    if (jobs['kind'] === 'success') {
      jobs['jobs'].forEach(e => {
        let accordion_item = document.createElement('div');
        accordion_item.classList.add(['accordion-item']);

        let header = document.createElement('h2');
        header.classList.add(['accordion-header']);

        let accordion_button = document.createElement('button');
        accordion_button.classList.add('accordion-button');
        accordion_button.classList.add('collapsed');
        accordion_button.type = 'button';
        accordion_button.setAttribute('data-bs-toggle', 'collapse');
        accordion_button.setAttribute('data-bs-target', `#job-${e['job_number']}`);

        let accordion_title = document.createElement('h5');
        accordion_title.innerText = `Job #${e['job_number']}`;
        let accordion_subtitle = document.createElement('h6');
        accordion_subtitle.innerText = `${e['start_date']} | ${e['start_time']}`;

        accordion_button.appendChild(accordion_title);
        accordion_button.appendChild(document.createElement('br'));
        accordion_button.appendChild(accordion_subtitle);
        header.appendChild(accordion_button);

        accordion_item.appendChild(header);

        let accordion_div = document.createElement('div');
        accordion_div.id = `job-${e['job_number']}`;
        accordion_div.classList.add('accordion-collapse');
        accordion_div.classList.add('collapse');

        let accordion_body = document.createElement('div');
        accordion_body.classList.add('accordion-body');
        accordion_body.innerText = "";

        accordion_body.innerText += `Harness: ${e['harness']}`;

        accordion_div.appendChild(accordion_body);
        accordion_item.appendChild(accordion_div);

        job_list_element.appendChild(accordion_item);
      });
    }
  }

  async function populate_combobox(dropdown, endpoint, selector) {
    const elements = await (await fetch(endpoint)).json();
    selector.innerHTML = '';
    elements.forEach(element => {
      const attributes = document.createElement('a');
      attributes.classList.add('dropdown-item');
      attributes.innerText = element;
      attributes.onclick = () => {
        dropdown.innerText = element;
      }
      selector.appendChild(attributes);
    })
  }

  function populate_harnesses() {
    populate_combobox(harness_dropdown_button, "/api/harnesses", harness_selector);
  }

  function populate_glitch_types() {
    populate_combobox(glitch_dropdown_button, "/api/glitch_types", glitch_types_selector);
  }

  refresh_harness_button.onclick = populate_harnesses;
  refresh_glitch_button.onclick = populate_glitch_types;

  gantry_forward_button.onclick = () => move_emp_relative(0, parseFloat(gantry_step.value), 0);
  gantry_backwards_button.onclick = () => move_emp_relative(0, -parseFloat(gantry_step.value), 0);
  gantry_left_button.onclick = () => move_emp_relative(-parseFloat(gantry_step.value), 0, 0);
  gantry_right_button.onclick = () => move_emp_relative(gantry_step.value, 0, 0);
  gantry_commit_button.onclick = () => {
    coordinates = gantry_coordinates.map(e => e.value);
    move_emp_absolute(coordinates[0], coordinates[1], coordinates[2]);
  }

  gantry_up_button.onclick = () => move_emp_relative(0, 0, parseFloat(gantry_step.value));
  gantry_down_button.onclick = () => move_emp_relative(0, 0, -parseFloat(gantry_step.value));

  job_submit.onclick = async () => {
    let job_data = {
      job_type: "emfi",
      harness: "simpleserial",
      job_parameters: {
        x: {
          minimum: document.getElementById('X-Minimum').value,
          maximum: document.getElementById('X-Maximum').value,
          step: document.getElementById('X-Step').value
        },
        y: {
          minimum: document.getElementById('Y-Minimum').value,
          maximum: document.getElementById('Y-Maximum').value,
          step: document.getElementById('Y-Step').value
        },
        z: {
          minimum: document.getElementById('Z-Minimum').value,
          maximum: document.getElementById('Z-Maximum').value,
          step: document.getElementById('Z-Step').value
        },
        ext_offset: {
          minimum: document.getElementById('Ext-Offset-Minimum').value,
          maximum: document.getElementById('Ext-Offset-Maximum').value,
          step: document.getElementById('Ext-Offset-Step').value
        },
        repeat: {
          minimum: document.getElementById('Repeat-Minimum').value,
          maximum: document.getElementById('Repeat-Maximum').value,
          step: document.getElementById('Repeat-Step').value
        },
        tries: {
          minimum: document.getElementById('Tries-Minimum').value,
          maximum: document.getElementById('Tries-Maximum').value,
          step: document.getElementById('Tries-Step').value
        }
      },
    };

    let result = await fetch(`/api/jobs/start`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(job_data)
    });
    let result_json = await result.json();
    if (result_json['kind'] === 'success') {
      // ...
    }
  };

  gantry_home_button.onclick = async () => {
    let result = await fetch(`/api/xyz-plane/home`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    let result_json = await result.json();
    if (result_json['kind'] === 'success') {
      update_coordinates(result_json);
    }
  }

  emp_arm_button.onclick = async () => {
    await fetch(`/api/emp/arm`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
  };
  emp_disarm_button.onclick = async () => {
    await fetch(`/api/emp/disarm`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
  };
  emp_fire_button.onclick = async () => {
    await fetch(`/api/emp/fire`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
  };

  build_parameter_table();
  get_current_coordinates();
  populate_job_history();
}