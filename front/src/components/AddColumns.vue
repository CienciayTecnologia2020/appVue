<template>
  <v-container>
    <v-row>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-btn  @click="triggerFileInput" class="load-button">Load Scenario from NovaDM</v-btn>
        <div class="button-group">
          <v-btn  @click="addInput">Add Parameter</v-btn>
          <v-btn  @click="addScenario">Add Scenario</v-btn>
          
          
          <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none;" />
        </div>
        <v-simple-table class="input-table">
          <thead>
            <tr>
              <th>Parameter Name</th>
              <th v-for="(scenario, index) in scenarios" :key="scenario.id_scenario">
                <div @click="editScenario(index)">
                  <v-text-field
                    v-if="editableScenarioIndex === index"
                    v-model="scenario.name_scenario"
                    outlined
                    dense
                    hide-details
                    class="scenario-header"
                    @blur="saveScenario(index)"
                    @keyup.enter="saveScenario(index)"
                  ></v-text-field>
                  <span v-else class="scenario-name">{{ scenario.name_scenario }}</span>
                </div>
                <v-btn icon small @click="removeScenario(scenario.id_scenario)">
                  <v-icon small>mdi-delete</v-icon>
                </v-btn>
              </th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(input, inputIndex) in inputs" :key="inputIndex">
              <td>
                <div @click="editInput(inputIndex)">
                  <v-text-field
                    v-if="editableInputIndex === inputIndex"
                    v-model="input.name"
                    outlined
                    dense
                    hide-details
                    class="parameter-header"
                    @blur="saveParameter(input.id_parameter, scenario, input)"
                    @keyup.enter="saveParameter(input.id_parameter, scenario, input)"
                  ></v-text-field>
                  <span v-else class="parameter-name">{{ input.name }}</span>
                </div>
              </td>
              <td v-for="(value, scenario) in input.values" :key="scenario">
                <v-text-field
                  v-model="input.values[scenario]"
                  outlined
                  dense
                  @blur="saveParameter(input.id_parameter, scenario, input)"
                  @keyup.enter="saveParameter(input.id_parameter, scenario, input)"
                ></v-text-field>
              </td>
              <td>
                <v-btn icon small @click="removeInput(inputIndex)">
                  <v-icon small>mdi-delete</v-icon>
                </v-btn>
              </td>
            </tr>
          </tbody>
        </v-simple-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

const apiUrl = process.env.VUE_APP_API_URL;

export default {
  props: ['selectedProblem'],
  data() {
    return {
      scenarios: [],
      inputs: [],
      editableScenarioIndex: null,
      editableInputIndex: null,
      showSaveButton: false,
    };
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
      
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = this.processFile;
      reader.readAsText(file);
    },
    processFile(event) {
      const fileContent = event.target.result;
      const scenarios = this.parseFileContent(fileContent);
      this.scenarios = scenarios;
      this.inputs = [];

      scenarios.forEach(scenario => {
        scenario.parameters.forEach(param => {
          const existingInput = this.inputs.find(input => input.name === param.name);
          if (existingInput) {
            existingInput.values[scenario.id_scenario] = param.value;
          } else {
            this.inputs.push({
              name: param.name,
              values: { [scenario.id_scenario]: param.value },
              id_parameter: param.id,
            });
          }
        });
      });

      this.showSaveButton = true;
      this.saveTable();
    },
    parseFileContent(content) {
      const lines = content.split('\n');
      const scenarios = {};
      let currentScenario = null;
      let paramId = 0;

      lines.forEach(line => {
        if (line.trim() === '') return;

        const [key, value] = line.split('=');

        if (key.toUpperCase() === key) {
          currentScenario = key.trim();
          scenarios[currentScenario] = {
            id_scenario: `temp_${Object.keys(scenarios).length}`,
            name_scenario: currentScenario,
            parameters: [],
          };
        } else if (currentScenario) {
          scenarios[currentScenario].parameters.push({
            id: `param_${paramId++}`,
            name: key.trim(),
            value: value.trim(),
          });
        }
      });

      return Object.values(scenarios);
    },
    async loadScenario() {
      try {
        const response = await axios.get(`${apiUrl}/scenario/${this.selectedProblem}`);
        const data = response.data;

        this.scenarios = data.map(item => ({
          id_scenario: item.id_scenario,
          name_scenario: item.name_scenario,
        }));

        this.inputs = [];

        data.forEach(item => {
          item.name_parameter.forEach((parameterName, index) => {
            const existingInput = this.inputs.find(input => input.name === parameterName);
            if (existingInput) {
              existingInput.values[item.id_scenario] = item.scenario_value[index];
              existingInput.id_parameter = item.id_parameter[index];
            } else {
              this.inputs.push({
                name: parameterName,
                values: { [item.id_scenario]: item.scenario_value[index] },
                id_parameter: item.id_parameter[index],
              });
            }
          });
        });
      } catch (error) {
        console.error('Error fetching scenario:', error);
      }
    },
    async addScenario() {
      try {
        const response = await axios.post(`${apiUrl}/scenario`, {
          name: `New Scenario ${this.scenarios.length + 1}`,
          problem_id: this.selectedProblem,
        });
        const newScenario = response.data;
        this.scenarios.push(newScenario);
        this.inputs.forEach(input => {
          input.values[newScenario.id_scenario] = '';
        });
        this.loadScenario();
      } catch (error) {
        console.error('Error creating scenario:', error);
        alert('Failed to create scenario.');
      }
    },
    async addInput() {
      const newInput = {
        name: 'New Parameter',
        values: {},
      };
      this.scenarios.forEach(scenario => {
        newInput.values[scenario.id_scenario] = '';
      });
      this.inputs.push(newInput);

      try {
        const response = await axios.post(`${apiUrl}/parameter`, {
          name: newInput.name,
          problem_id: this.selectedProblem,
        });
        const createdParameter = response.data;
        newInput.id_parameter = createdParameter.parameter_id;
        this.loadScenario();
      } catch (error) {
        console.error('Error adding parameter:', error);
        alert('Failed to add parameter.');
      }
    },
    async removeScenario(scenarioId) {
      try {
        await axios.delete(`${apiUrl}/delete-scenario/${scenarioId}`);
        const index = this.scenarios.findIndex(scenario => scenario.id_scenario === scenarioId);
        if (index !== -1) {
          this.scenarios.splice(index, 1);
          this.inputs.forEach(input => {
            delete input.values[scenarioId];
          });
        }
      } catch (error) {
        console.error('Error deleting scenario:', error);
        alert('Failed to delete scenario.');
      }
    },
    async removeInput(index) {
      const parameterToRemove = this.inputs[index].id_parameter;
      if (parameterToRemove) {
        try {
          await axios.delete(`${apiUrl}/delete-parameter/${parameterToRemove}`);
          this.inputs.splice(index, 1);
        } catch (error) {
          console.error('Error deleting parameter:', error);
          alert('Failed to delete parameter.');
        }
      } else {
        this.inputs.splice(index, 1);
      }
    },
    editScenario(index) {
      this.editableScenarioIndex = index;
    },
    async saveScenario(index) {
      const scenario = {
        id_scenario: this.scenarios[index].id_scenario,
        name_scenario: this.scenarios[index].name_scenario,
        problem_id: this.selectedProblem,
      };

      try {
        const method = scenario.id_scenario ? 'PUT' : 'POST';
        const endpoint = scenario.id_scenario
          ? `${apiUrl}/scenario/${scenario.id_scenario}`
          : `${apiUrl}/scenario`;

        const response = await fetch(endpoint, {
          method,
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: scenario.name_scenario,
            problem_id: scenario.problem_id,
          }),
        });

        if (response.ok) {
          const responseData = await response.json();
          if (!scenario.id_scenario) {
            this.scenarios[index].id_scenario = responseData.id_scenario;
          }
          this.editableScenarioIndex = null;
        } else {
          console.error('Failed to save scenario');
        }
      } catch (error) {
        console.error('Error saving scenario:', error);
      }
    },
    editInput(index) {
      this.editableInputIndex = index;
    },
    async saveInput(index) {
      const input = {
        id_parameter: this.inputs[index].id_parameter,
        name: this.inputs[index].name,
        problem_id: this.selectedProblem,
      };

      try {
        // Use PUT for input name updates
        const method = 'PUT';
        const endpoint = `${apiUrl}/parameter/${input.id_parameter}`;

        const response = await fetch(endpoint, {
          method,
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(input),
        });

        if (response.ok) {
          const responseData = await response.json();
          if (!input.id_parameter) {
            this.inputs[index].id_parameter = responseData.parameter_id;
          }
          this.editableInputIndex = null;
        } else {
          console.error('Failed to save input');
        }
      } catch (error) {
        console.error('Error saving input:', error);
      }
    },
    async saveParameter(parameterId, scenarioId, input) {
      try {
        // Use PUT for parameter values
        const method = 'PUT';
        const endpoint = `${apiUrl}/parameter/${parameterId}`;

        const response = await fetch(endpoint, {
          method,
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            value: input.values[scenarioId],
            name: input.name,
            problem_id: this.selectedProblem,
            scenario_id: scenarioId,
          }),
        });

        if (response.ok) {
          const responseData = await response.json();
          if (!parameterId) {
            input.id_parameter = responseData.parameter_id;
          }
        } else {
          console.error('Failed to save parameter');
        }
      } catch (error) {
        console.error('Error saving parameter:', error);
      }
    },
    async saveTable() {
      try {
        const data = {
          problem_id: this.selectedProblem,
          scenarios: this.scenarios,
          inputs: this.inputs,
        };

        const response = await axios.post(`${apiUrl}/save-table`, data);

        if (response.status === 200) {
          alert('Table saved successfully');
          this.loadScenario();
        } else {
          console.error('Failed to save table:', response.data.error);
          alert('Failed to save table.');
        }
      } catch (error) {
        console.error('Error saving table:', error);
        alert('Failed to save table.');
      } finally {
        this.showSaveButton = false;
      }
    },
  },
  mounted() {
  this.loadScenario();
},
  
};
</script>

<style scoped>
.load-button,
.button-group .v-btn {
  height: 40px;
  line-height: 40px;
  box-sizing: border-box;
  margin-bottom: 10px;
  margin-top: 10px;
  border: 2px solid rgb(44, 182, 125);
  background-color: transparent;
  color: rgb(44, 182, 125);
  font-size: 12px;
  cursor: pointer;
  text-align: left; /* Alineación a la izquierda */
  padding-left: 10px; /* Espaciado a la izquierda para mejorar la alineación */
}

.load-button:hover,
.button-group .v-btn:hover {
  background-color: rgb(44, 182, 125);
  color: white;
}

.button-group {
  display: flex;
  gap: 10px; /* Espaciado entre los botones */
}


.input-table {
  border: 1px solid #ccc;
  border-collapse: collapse;
  width: 100%;
}

.input-table th,
.input-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}

.input-table th {
  background-color: #f9f9f9;
}

.input-table td {
  background-color: #fff;
}

.scenario-header,
.parameter-header {
  max-width: none;
  margin-right: 5px;
}

.scenario-name,
.parameter-name {
  font-weight: bold;
  cursor: pointer;
}

.v-btn.v-size--small {
  height: 24px;
  width: 24px;
}
</style>
