<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card-title class="fixed-label">
        
        </v-card-title>
        <!-- Menú desplegable para seleccionar KPIs -->
        

        <!-- Botones de crear nuevo y guardar cambios -->
        
        
      </v-col>
      <v-col cols="4">
        <div>
          <v-btn @click="createNewItem" class="create-bottom">CREATE NEW</v-btn>
          <select v-model="selectedKPI" @change="selectKPI" class="custom-select">
            <option :value="null" disabled class="center-select-option">Select a KPI</option>
            <option v-for="kpi in kpis" :value="kpi.id" :key="kpi.id">{{ kpi.name }}</option>
          </select>
        </div>
        <!-- Lista estática de KPIs seleccionados -->
        <v-list v-if="selectedKPIList.length > 0">
          <h3>Selected KPIs</h3>
          <v-list-item
            v-for="kpi in selectedKPIList"
            :key="kpi.id"
            @click="viewKPIDetails(kpi)"
            :class="{ 'selected': kpi.id === selectedKPI }"
          >
            <v-list-item-content>
              <v-list-item-title>{{ kpi.name }}</v-list-item-title>
              <v-list-item-subtitle>Unit: {{ kpi.unit }}</v-list-item-subtitle>
              <v-list-item-subtitle>Pillar: {{ kpi.pillar }}</v-list-item-subtitle>
            </v-list-item-content>
            <!-- Botón de eliminar -->
            <v-icon @click.stop="removeFromSelectedItemList(kpi.id)" color="red">mdi-close-circle</v-icon>
          </v-list-item>
        </v-list>
      </v-col>

      <v-col cols="8">
        <v-card-title class="fixed-label">
          <span>KPI Information</span>
        </v-card-title>
              <!-- Mostrar las características del KPI seleccionado -->
        <div>
          <v-text-field v-model="name" label="Name"></v-text-field>
          <v-text-field v-model="unit" label="Unit"></v-text-field>
          <v-text-field v-model="pillar" label="Pillar"></v-text-field>
          <v-textarea v-model="impact" label="Impact" outlined rows="3"></v-textarea>
          <v-card class="label-button-container">
            <v-card-text class="item-label">
              <span>Base Line Needed</span>
            </v-card-text>
            <v-card-text class="item-button">
              <v-btn @click="toggleBaseLineDataNeeded" :color="baseLineDataNeeded ? 'success' : 'error'" outlined>
                {{ baseLineDataNeeded ? 'Yes' : 'No' }}
              </v-btn>
            </v-card-text>
            
          </v-card>
          <lifeCycleSelection :selectedKPI="selectedKPI" />
          <v-card-title class="fixed-label">
            <span>KPI Responsibility</span>
          </v-card-title>
          <v-text-field v-model="responsibilityDefinition" label="Definition"></v-text-field>
          <v-text-field v-model="responsibilityCalculation" label="Calculation"></v-text-field>
          <v-card-title class="fixed-label">
            <span>KPI Description</span>
          </v-card-title>
          <v-textarea v-model="description" label="Description" outlined rows="3"></v-textarea>
          <v-textarea v-model="dataRequirements" label="Data Requirements" outlined rows="3"></v-textarea>
          <v-textarea v-model="formula" label="Formula" outlined rows="3"></v-textarea>
          <!-- Botón de eliminar -->
          <v-btn v-if="selectedKPI" @click.stop="confirmDeleteKPI(selectedKPI)" color="red">Delete</v-btn>
          <v-btn @click="saveKPI" color="yellow" block class="mt-4">Save Changes</v-btn>
        </div>
      </v-col>
    </v-row>

    <!-- Diálogo de confirmación -->
    <v-dialog v-model="confirmDialog" max-width="400">
      <v-card>
        <v-card-title>Confirm Delete</v-card-title>
        <v-card-text>Are you sure you want to delete this KPI?</v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="deleteKPI">Yes</v-btn>
          <v-btn color="red" @click="confirmDialog = false">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-snackbar v-model="snackbar" :timeout="snackbarTimeout" color="success">
      Changes saved successfully!
      <v-btn text @click="snackbar = false">Close</v-btn>
    </v-snackbar>
  </v-container>
</template>

<script>


import lifeCycleSelection from '/src/components/lifeCycleSelection.vue';

export default {
  props: ['selectedLab', 'selectedProblem'],
  components: {
    lifeCycleSelection
  },
  data() {
    return {
      apiUrl: process.env.VUE_APP_API_URL, 
      unit: '',
      pillar: '',
      calculationFrequency: '',
      name: '',
      impact: '',
      baseLineDataNeeded: null,
      lifecycle: '',
      responsibilityDefinition: '',
      responsibilityCalculation: '',
      description: '',
      dataRequirements: '',
      formula: '',
      selectedKPI: null,
      selectedKPIList: [],
      kpis: [],
      savedKPIs: [],
      confirmDialog: false,
      kpiToDelete: null,
      snackbar: false,
      lifeCycles: [], // Nueva propiedad para los lifeCycles
      selectedLifeCycle: null,
      snackbarTimeout: 3000
    };
  },
  methods: {
    onProblemSelected(selectedKPI) {
      this.selectedKPI = selectedKPI;
    },
    confirmDeleteKPI(kpiId) {
      this.kpiToDelete = kpiId;
      this.confirmDialog = true;
    },
    async deleteKPI() {
      try {
        
        const response = await fetch(`${this.apiUrl}/kpi/${this.kpiToDelete}`, {
          method: 'DELETE',
          headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        selectedProblem: this.selectedProblem
      })
    });
        if (response.ok) {
          this.fetchKPIs();
          this.removeFromSelectedKPIList(this.kpiToDelete);
          this.confirmDialog = false;
        } else {
          console.error('Error deleting KPI:', response.statusText);
        }
      } catch (error) {
        console.error('Error deleting KPI:', error);
      }
    },
    async createNewItem() {
  this.clearKPIDetails();
  const newTempKPI = {
    id: 'temp-' + new Date().getTime(),
    name: 'New KPI',
    baseLineDataNeeded: 'True',
    formula: '',
    impact: '',
    lifecycle: '',
    responsibilityDefinition: '',
    responsibilityCalculation: '',
    description: '',
    dataRequirements: '',

    temp: true
  };

  this.selectedKPIList.push(newTempKPI);
  this.viewKPIDetails(newTempKPI);

  try {
    const response = await fetch(`${this.apiUrl}/kpi`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: newTempKPI.name,
        baseLineDataNeeded: newTempKPI.baseLineDataNeeded,
        formula: newTempKPI.formula,
        lifecycle: newTempKPI.lifecycle,
        responsibilityDefinition: newTempKPI.responsibilityDefinition,
        responsibilityCalculation: newTempKPI.responsibilityCalculation,
        description: newTempKPI.description,
        dataRequirements: newTempKPI.dataRequirements,
        impact: newTempKPI.impact,
        selectedProblem: this.selectedProblem,
        selectedLab: this.selectedLab
      })
    });

    if (response.ok) {
      // Recibir el stakeholder creado desde el servidor
      const createdKPI = await response.json();
      // Actualizar el id del stakeholder temporal con el id recibido del servidor
      newTempKPI.id = createdKPI.id;

      

      // Eliminar el atributo temporal del stakeholder una vez que se ha creado en el servidor
      delete newTempKPI.temp;

      // Actualizar la lista de stakeholders después de crear el nuevo stakeholder
      this.fetchKPIs();

      // Seleccionar el nuevo stakeholder creado
      this.selectedKPI = createdKPI.id;
    } else {
      console.error('Error creating new KPI:', response.statusText);
    }
  } catch (error) {
    console.error('Error creating new KPI:', error);
  }
}
,
    createNewKPI() {
      this.unit = '';
      this.pillar = '';
      this.calculationFrequency = '';
      this.name = '';
      this.impact = '';
      this.baseLineDataNeeded = null;
      this.lifecycle = '';
      this.responsibilityDefinition = '';
      this.responsibilityCalculation = '';
      this.description = '';
      this.dataRequirements = '';
      this.formula = '';
      this.selectedKPI = null;

      const newTempKPI = {
        id: 'temp-' + new Date().getTime(),
        name: 'New KPI',
        temp: true
      };
      this.selectedKPIList.push(newTempKPI);
    },
    async fetchKPIs() {
      // Obtener KPIs
      if (this.selectedProblem) {
        try {
          const response = await fetch(`${this.apiUrl}/kpi/${this.selectedProblem}`);
          const data = await response.json();
          this.kpis = data;
          this.selectedKPIList = this.kpis.filter(kpi => kpi.selectedKpi);
        } catch (error) {
          console.error('Error fetching KPIs:', error);
          this.kpis = [];
        }
      }
      // Obtener lifeCycles
      try {
        const response = await fetch(`${this.apiUrl}/lifecycle`);
        const data = await response.json();
        this.lifeCycles = data;
      } catch (error) {
        console.error('Error fetching lifeCycles:', error);
        this.lifeCycles = [];
      }
    },
    async selectKPI() {
      if (this.selectedKPI) {
        const selectedKPIData = this.kpis.find(kpi => kpi.id === this.selectedKPI);
        this.addToSelectedItemList(selectedKPIData);
        if (selectedKPIData) {
          this.unit = selectedKPIData.unit;
          this.pillar = selectedKPIData.pillar;
          this.calculationFrequency = selectedKPIData.calculationFrequency;
          this.formula = selectedKPIData.formula;
          this.description = selectedKPIData.description;
          this.dataRequirements = selectedKPIData.dataRequirements;
          this.responsibilityDefinition = selectedKPIData.responsibilityDefinition;
          this.responsibilityCalculation = selectedKPIData.responsibilityCalculation;
          this.name = selectedKPIData.name;
          this.impact = selectedKPIData.impact;
          this.baseLineDataNeeded = selectedKPIData.baseLineDataNeeded === "True";
          this.lifecycle = selectedKPIData.lifecycle;
          // Aquí se actualiza el selectedLifeCycle
          this.selectedLifeCycle = selectedKPIData.lifecycle_id;
          this.addToSelectedKPIList(selectedKPIData);
        }
      }
    },
    async updateLifeCycle() {
      if (this.selectedKPI && this.selectedLifeCycle) {
        try {
          const response = await fetch(`${this.apiUrl}/lifecycle/${this.selectedKPI}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ lifecycle_id: this.selectedLifeCycle })
          });
          if (!response.ok) {
            console.error('Error updating lifecycle:', response.statusText);
          }
        } catch (error) {
          console.error('Error updating lifecycle:', error);
        }
      }
    },
    addToSelectedKPIList(kpi)  {
      if (!this.selectedKPIList.find(item => item.id === kpi.id)) {
        this.selectedKPIList.push(kpi);
      }
    },
    removeFromSelectedKPIList(kpiId) {
  const index = this.selectedKPIList.findIndex(item => item.id === kpiId);
  if (index !== -1) {
    this.selectedKPIList.splice(index, 1);
    const nextKPI = this.selectedKPIList[index] || this.selectedKPIList[index - 1];
    if (nextKPI) {
      this.viewKPIDetails(nextKPI);
    } else {
      // Si no hay más KPIs en la lista, limpiamos los detalles
      this.clearKPIDetails();
    }
  }
},




  clearKPIDetails() {
    this.name = '';
    this.unit = '';
    this.pillar = '';
    this.calculationFrequency = '';
    this.impact = '';
    this.baseLineDataNeeded = null;
    this.lifecycle = '';
    this.responsibilityDefinition = '';
    this.responsibilityCalculation = '';
    this.description = '';
    this.dataRequirements = '';
    this.formula = '';
    this.selectedKPI = null;
  },
    viewKPIDetails(kpi) {
      this.selectedKPI = kpi.id;
      this.unit = kpi.unit;
      this.pillar = kpi.pillar;
      this.calculationFrequency = kpi.calculationFrequency;
      this.formula = kpi.formula;
      this.description = kpi.description;
      this.dataRequirements = kpi.dataRequirements;
      this.responsibilityDefinition = kpi.responsibilityDefinition;
      this.responsibilityCalculation = kpi.responsibilityCalculation;
      this.name = kpi.name;
      this.impact = kpi.impact;
      this.baseLineDataNeeded = kpi.baseLineDataNeeded === "True";
      this.lifecycle = kpi.lifecycle;
      // Aquí se actualiza el selectedLifeCycle
      this.selectedLifeCycle = kpi.lifecycle_id;
    },
    async saveKPI() {
  const kpiData = {
    id: this.selectedKPI,
    selectedLab: this.selectedLab,
    name: this.name,
    unit: this.unit,
    pillar: this.pillar,
    calculationFrequency: this.calculationFrequency,
    impact: this.impact,
    baseLineDataNeeded: this.baseLineDataNeeded ? "True" : "False",
    lifecycle: this.lifecycle,
    responsibilityDefinition: this.responsibilityDefinition,
    responsibilityCalculation: this.responsibilityCalculation,
    description: this.description,
    dataRequirements: this.dataRequirements,
    formula: this.formula,
    selectedProblem: this.selectedProblem,
    selectedKPI: this.selectedKPIList.map(kpi => kpi.id)

  };

  const OneapiUrl = this.selectedKPI ? `${this.apiUrl}/kpi/${this.selectedKPI}` : `${this.apiUrl}/kpi`;
  const method = this.selectedKPI ? 'PUT' : 'POST';

  try {
    const response = await fetch(OneapiUrl, {
      method: method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(kpiData)
    });
    
    if (response.ok) {
      const responseData = await response.json();

      if (!this.selectedKPI) {
        this.selectedKPI = responseData.id;
      }

      const updatedKPI = {
        id: this.selectedKPI,
        name: this.name,
        unit: this.unit,
        pillar: this.pillar,
        calculationFrequency: this.calculationFrequency,
        impact: this.impact,
        baseLineDataNeeded: this.baseLineDataNeeded ? "True" : "False",
        lifecycle: this.lifecycle,
        responsibilityDefinition: this.responsibilityDefinition,
        responsibilityCalculation: this.responsibilityCalculation,
        description: this.description,
        dataRequirements: this.dataRequirements,
        formula: this.formula,
        selectedProblem: this.selectedProblem,
        selectedKPI: this.selectedKPIList.map(kpi => kpi.id)
            
      };

      const index = this.savedKPIs.findIndex(item => item.id === this.selectedKPI);
      if (index !== -1) {
        this.savedKPIs.splice(index, 1, updatedKPI);
      } else {
        this.savedKPIs.push(updatedKPI);
      }

      const staticIndex = this.selectedKPIList.findIndex(item => item.id === this.selectedKPI);
      if (staticIndex !== -1) {
        this.selectedKPIList.splice(staticIndex, 1, updatedKPI);
      } else {
        this.selectedKPIList.push(updatedKPI);
      }

      this.fetchKPIs();
      this.snackbar = true; // Mostrar la notificación
    } else {
      console.error('Error saving KPI:', response.statusText);
    }
  } catch (error) {
    console.error('Error saving KPI:', error);
  }
}

,
    updateSelectedKPIList(updatedKPI) {
      const index = this.selectedKPIList.findIndex(kpi => kpi.id === updatedKPI.id);
      if (index !== -1) {
        this.$set(this.selectedKPIList, index, updatedKPI);
        // Buscamos y actualizamos el KPI en la lista estática
        const selectedKPIIndex = this.selectedKPIList.findIndex(kpi => kpi.id === updatedKPI.id);
        if (selectedKPIIndex !== -1) {
          this.selectedKPIList.splice(selectedKPIIndex, 1, updatedKPI);
        }
      } else {
        this.selectedKPIList.push(updatedKPI);
      }
    },
    async addToSelectedItemList(kpi) {
      if (!this.selectedKPIList.find(item => item.id === kpi.id)) {
        this.selectedKPIList.push(kpi);
        try {
          const response = await fetch(`${this.apiUrl}/add-kpi/${kpi.id}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ selectedProblem: this.selectedProblem })
          });
          if (!response.ok) {
            console.error('Error adding KPI to list:', response.statusText);
          }
        } catch (error) {
          console.error('Error adding KPI to list:', error);
        }
      }
    },
    async removeFromSelectedItemList(kpiId) {
      const index = this.selectedKPIList.findIndex(item => item.id === kpiId);
      if (index !== -1) {
        this.selectedKPIList.splice(index, 1);
        try {
          const response = await fetch(`${this.apiUrl}/delete-kpi/${kpiId}`, {
            method: 'DELETE'
          });
          if (!response.ok) {
            console.error('Error removing building from list:', response.statusText);
          }
        } catch (error) {
          console.error('Error removing building from list:', error);
        }
        if (this.selectedKPI === kpiId) {
          const previousIndex = index > 0 ? index - 1 : null;
          this.selectedKPI = previousIndex !== null ? this.selectedKPIList[previousIndex].id : null;
          if (this.selectedKPI) {
            this.viewKPIDetails(this.selectedKPIList[previousIndex]);
          } else {
            this.clearKPIDetails();
          }
        }
      }
      
      // Si no hay ningún building seleccionado después de la eliminación, seleccionamos el último building restante
      if (!this.selectedKPI && this.selectedKPIList.length > 0) {
        this.selectedKPI = this.selectedKPIList[this.selectedKPIList.length - 1].id;
        this.viewKPIDetails(this.selectedKPIList[this.selectedKPIList.length - 1]);
      }
    },
    async deleteItem() {
      try {
        const response = await fetch(`${this.apiUrl}/delete-kpi/${this.kpiToDelete}`, {
          method: 'DELETE'
        });
        if (response.ok) {
          this.removeFromSelectedStakeholderList(this.kpiToDelete);
          this.confirmDialog = false;
          this.snackbar = true;
        } else {
          console.error('Error deleting KPI:', response.statusText);
        }
      } catch (error) {
        console.error('Error deleting KPI:', error);
      }
    },
    toggleBaseLineDataNeeded() {
      this.baseLineDataNeeded = !this.baseLineDataNeeded;
    }
  },
  watch: {
    selectedProblem(newProblemId, oldProblemId) {
    if (newProblemId !== oldProblemId) {
      this.fetchKPIs();
    }
  },
    selectedLab: {
      immediate: true,
      handler(newValue) {
        if (newValue) {
          this.fetchKPIs();
        }
      }
    }
  }
};
</script>




<style scoped>
.kpi-selection {
  margin-top: 15px;
}

.custom-select {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #c0e8c6;
  border-radius: 0.25rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.custom-select:focus {
  border-color: #50ff76;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(1, 20, 8, 0.25);
}

.fixed-label {
  font-weight: bold;
}

.item-label {
  font-size: medium;
  text-align: left;
  color: #8b8b8b;
}

.label-button-container {
  background-color: #f2f2f2;
  border-radius: 4px;
  padding: 8px;
  margin-bottom: 15px;
}

.item-button {
  padding-top: 0;
  padding-bottom: 0;
}

.selected {
  background-color: rgb(44, 182, 125);
  font-weight: bold;
  color: white;
}

h3 { 
  margin-bottom: 1rem;
  margin-top: 20px;
  color: black;
}

.v-btn.create-bottom {
  width: 100%;
  height: 40px; /* Ajusta según la altura del select */
  line-height: 40px; /* Centra el texto verticalmente */
  box-sizing: border-box;
  margin-bottom: 20px;
  border: 2px solid rgb(44, 182, 125);
  background-color: transparent;
  color: rgb(44, 182, 125);
  font-size: 12px;
  cursor: pointer;

}


.v-btn.create-bottom:hover {
  background-color: rgb(44, 182, 125);
  color: white;
}
.center-select-option {
  text-align: center;
}
</style>

