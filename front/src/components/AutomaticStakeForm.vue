<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card-title class="fixed-label">
          
        </v-card-title>
        <!-- Menú desplegable para seleccionar Stakeholders -->

        <!-- Lista de Stakeholders guardados -->
        <v-row v-if="savedStakeholders.length > 0">
          <!-- Aquí podrías agregar un componente para mostrar los savedStakeholders -->
        </v-row>
      </v-col>
      
      <v-col cols="4">
        <div>
          <!-- Botones de crear nuevo y guardar cambios -->
          <v-btn @click="createNewItem"  class="add">CREATE NEW</v-btn>
          <select v-model="selectedStakeholder" @change="selectStakeholder" class="custom-select">
            <option :value="null" disabled class="center-select-option">Select a Stakeholder</option>
            <option v-for="stakeholder in stakeholders" :value="stakeholder.id" :key="stakeholder.id">{{ stakeholder.name }}</option>
          </select>

          <v-btn @click="createNewGPTItem"  :disabled="isLoading" class="add">
            <v-icon v-if="isLoading">mdi-loading mdi-spin</v-icon>
            <span v-else>USE GPT</span>
          </v-btn>
        </div>
        <!-- Lista estática de Stakeholders seleccionados -->
        <v-list v-if="selectedStakeholderList.length > 0">
          <h3>Selected Stakeholders</h3>
          <v-list-item
            v-for="stakeholder in selectedStakeholderList"
            :key="stakeholder.id"
            @click="viewStakeholderDetails(stakeholder)"
            :class="{ 'selected': stakeholder.id === selectedStakeholder || stakeholder.temp }"
          >
            <v-list-item-content>
              <v-list-item-title>{{ stakeholder.name }}</v-list-item-title>
              <!--<v-list-item-subtitle>Specificities: {{ stakeholder.specificities }}</v-list-item-subtitle> -->
              <v-list-item-subtitle>Requirements: {{ stakeholder.requirements }}</v-list-item-subtitle>
            </v-list-item-content>
            <!-- Botón de eliminar -->
            <v-icon v-if="stakeholder.specificities === 'Stakeholder generated with GPT-4o'">mdi-pencil</v-icon>

            <v-icon @click.stop="removeFromSelectedItemList(stakeholder.id)" color="red">mdi-close-circle</v-icon>
          </v-list-item>
        </v-list>
      </v-col>

      <v-col cols="8">
        <v-card-title class="fixed-label">
          <span>Stakeholder Information</span>
        </v-card-title>
        <!-- Mostrar las características del Stakeholder seleccionado -->
        <div>
          <v-text-field v-model="name" label="Name"></v-text-field>
          <!--<v-text-field v-model="specificities" label="Specificities"></v-text-field>-->
          <v-text-field v-model="generalDescription" label="General Description"></v-text-field>
          <v-text-field v-model="requirements" label="Requirements"></v-text-field>
          
          
          <!-- Botón de eliminar -->
          <v-btn v-if="selectedStakeholder" @click.stop="confirmDeleteStakeholder(selectedStakeholder)" color="red">Delete</v-btn>
          <v-btn @click="saveChanges" color="yellow" block class="mt-4">Save Changes</v-btn>
        </div>
      </v-col>
    </v-row>
    
    <!-- Diálogo de confirmación -->
    <v-dialog v-model="confirmDialog" max-width="400">
      <v-card>
        <v-card-title>Confirm Delete</v-card-title>
        <v-card-text>Are you sure you want to delete this Stakeholder?</v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="deleteStakeholder">Yes</v-btn>
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
export default {
  props: ['selectedLab', 'selectedProblem'],
  data() {
    return {
      name: '',
      apiUrl: process.env.VUE_APP_API_URL, 
      specificities: '',
      requirements: '',
      generalDescription: '',
      relatedKPI: '',
      selectedStakeholder: null,
      selectedStakeholderList: [],
      stakeholders: [],
      savedStakeholders: [],
      confirmDialog: false,
      stakeholderToDelete: null,
      snackbar: false,
      snackbarTimeout: 3000,
      isLoading: false,
      
    };
  },
  methods: {
    confirmDeleteStakeholder(stakeholderId) {
      this.stakeholderToDelete = stakeholderId;
      this.confirmDialog = true;
    },
    async deleteItem() {
      try {
        const response = await fetch(`${this.apiUrl}/delete-stakeholder/${this.stakeholderToDelete}`, {
          method: 'DELETE'
        });
        if (response.ok) {
          this.removeFromSelectedStakeholderList(this.stakeholderToDelete);
          this.confirmDialog = false;
          this.snackbar = true;
        } else {
          console.error('Error deleting Building:', response.statusText);
        }
      } catch (error) {
        console.error('Error deleting Building:', error);
      }
    },
    storeGeneratedStakeholders() {
    this.generatedStakeholders = this.stakeholders.filter(stakeholder => 
      stakeholder.specificities === 'Stakeholder generated with GPT-4'
    );
  },
    async addToSelectedItemList(stakeholder) {
      if (!this.selectedStakeholderList.find(item => item.id === stakeholder.id)) {
        this.selectedStakeholderList.push(stakeholder);
        try {
          const response = await fetch(`${this.apiUrl}/add-stakeholder/${stakeholder.id}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ selectedProblem: this.selectedProblem })
          });
          if (!response.ok) {
            console.error('Error adding stakeholder to list:', response.statusText);
          }
        } catch (error) {
          console.error('Error adding stakeholder to list:', error);
        }
      }
    },
    async deleteStakeholderGenerated(stakeholderId) {
      try {
        const response = await fetch(`${this.apiUrl}/stakeholder/${stakeholderId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          }
        });
        if (response.ok) {
          this.removeFromSelectedStakeholderList(stakeholderId);
          this.fetchStakeholders();
          
        } else {
          console.error('Error deleting Stakeholder:', response.statusText);
        }
      } catch (error) {
        console.error('Error deleting Stakeholder:', error);
      }
    },
    async deleteStakeholder() {
      try {
        const response = await fetch(`${this.apiUrl}/stakeholder/${this.stakeholderToDelete}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          }
        });
        if (response.ok) {
          this.fetchStakeholders();
          this.removeFromSelectedStakeholderList(this.stakeholderToDelete);
          this.confirmDialog = false;
        } else {
          console.error('Error deleting Stakeholder:', response.statusText);
        }
      } catch (error) {
        console.error('Error deleting Stakeholder:', error);
      }
    },

    async createNewItem() {
      this.clearStakeholderDetails();
      const newTempStake = {
        id: 'temp-' + new Date().getTime(),
        name: 'New Stakeholder',
        specificities: 'Specificities',
        requirements: 'Requirements',
        general_description: 'General Description',
        related_kpi: 'Related KPI',
        temp: true
      };

      this.selectedStakeholderList.push(newTempStake);
      this.viewStakeholderDetails(newTempStake);

      try {
        const response = await fetch(`${this.apiUrl}/stakeholder`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: newTempStake.name,
            specificities: newTempStake.specificities,
            requirements: newTempStake.requirements,
            general_description: newTempStake.general_description,
            related_kpi: newTempStake.related_kpi,
            selectedProblem: this.selectedProblem,
            selectedLab: this.selectedLab
          })
        });

        if (response.ok) {
          // Recibir el stakeholder creado desde el servidor
          const createdStakeholder = await response.json();
          // Actualizar el id del stakeholder temporal con el id recibido del servidor
          newTempStake.id = createdStakeholder.id;

          // Eliminar el atributo temporal del stakeholder una vez que se ha creado en el servidor
          delete newTempStake.temp;

          // Actualizar la lista de stakeholders después de crear el nuevo stakeholder
          this.fetchStakeholders();

          // Seleccionar el nuevo stakeholder creado
          this.selectedStakeholder = newTempStake.id;
        } else {
          console.error('Error creating new stakeholder:', response.statusText);
        }
      } catch (error) {
        console.error('Error creating new stakeholder:', error);
      }
    },
    async createNewGPTItem() {
  this.clearStakeholderDetails();
  this.isLoading = true; // Establecer el estado de carga en true

  try {
    const response = await fetch(`${this.apiUrl}/gpt-stakeholder`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        selectedProblem: this.selectedProblem,
        selectedLab: this.selectedLab
      })
    });

    if (response.ok) {
      const newGPTStakeholder = await response.json();
      this.selectedStakeholderList.push(newGPTStakeholder);
      this.viewStakeholderDetails(newGPTStakeholder);
    } else {
      console.error('Error creating new GPT stakeholder:', response.statusText);
    }
  } catch (error) {
    console.error('Error creating new GPT stakeholder:', error);
  } finally {
    this.isLoading = false; // Establecer el estado de carga en false
    this.fetchStakeholders();
  }
}
,
    createNewStakeholder() {
      this.name = '';
      this.specificities = '';
      this.requirements = '';
      this.generalDescription = '';
      this.relatedKPI = '';
      this.selectedStakeholder = null;

      const newTempStake = {
        id: 'temp-' + new Date().getTime(),
        name: 'New Stakeholder',
        specificities: 'Specificities',
        requirements: 'Requirements',
        general_description: 'General Description',
        related_kpi: 'Related KPI',
        temp: true
      };

      this.selectedStakeholderList.push(newTempStake);
    },
    async fetchStakeholders() {
      if (this.selectedProblem) {
        try {
          const response = await fetch(`${this.apiUrl}/stakeholder/${this.selectedProblem}`);
          const data = await response.json();
          this.stakeholders = data;

          this.selectedStakeholderList = this.stakeholders.filter(stakeholder => stakeholder.selectedStakeholder);

          console.log('Selected Stakeholders:', this.selectedStakeholderList);
          console.log('Stakeholders:', this.stakeholders);
        } catch (error) {
          console.error('Error fetching Stakeholders:', error);
          this.stakeholders = [];
        }
      }
    },
    async selectStakeholder() {
      if (this.selectedStakeholder) {

        const selectedStakeholderData = this.stakeholders.find(stakeholder => stakeholder.id === this.selectedStakeholder);
        this.addToSelectedItemList(selectedStakeholderData);
        if (selectedStakeholderData) {
          this.name = selectedStakeholderData.name;
          this.specificities = selectedStakeholderData.specificities;
          this.requirements = selectedStakeholderData.requirements;
          this.generalDescription = selectedStakeholderData.general_description;
          this.relatedKPI = selectedStakeholderData.related_kpi;
          this.addToSelectedStakeholderList(selectedStakeholderData);

        }
      }
    },
    async removeFromSelectedItemList(stakeholderId) {
      const index = this.selectedStakeholderList.findIndex(item => item.id === stakeholderId);
      if (index !== -1) {
        this.selectedStakeholderList.splice(index, 1);
        try {
          const response = await fetch(`${this.apiUrl}/delete-stakeholder/${stakeholderId}`, {
            method: 'DELETE'
          });
          if (!response.ok) {
            console.error('Error removing building from list:', response.statusText);
          }
        } catch (error) {
          console.error('Error removing building from list:', error);
        }
        if (this.selectedStakeholder === stakeholderId) {
          const previousIndex = index > 0 ? index - 1 : null;
          this.selectedStakeholder = previousIndex !== null ? this.selectedStakeholderList[previousIndex].id : null;
          if (this.selectedStakeholder) {
            this.viewStakeholderDetails(this.selectedStakeholderList[previousIndex]);
          } else {
            this.clearStakeholderDetails();
          }
        }
      }

      // Si no hay ningún building seleccionado después de la eliminación, seleccionamos el último building restante
      if (!this.selectedStakeholder && this.selectedStakeholderList.length > 0) {
        this.selectedStakeholder = this.selectedStakeholderList[this.selectedStakeholderList.length - 1].id;
        this.viewStakeholderDetails(this.selectedStakeholderList[this.selectedStakeholderList.length - 1]);
      }
    },
    addToSelectedStakeholderList(stakeholder) {
      if (!this.selectedStakeholderList.find(item => item.id === stakeholder.id)) {
        this.selectedStakeholderList.push(stakeholder);
      }
    },
    removeFromSelectedStakeholderList(stakeholderId) {
      const index = this.selectedStakeholderList.findIndex(item => item.id === stakeholderId);
      if (index !== -1) {
        this.selectedStakeholderList.splice(index, 1);
        const nextStakeholder = this.selectedStakeholderList[index] || this.selectedStakeholderList[index - 1];
        if (nextStakeholder) {
          this.viewStakeholderDetails(nextStakeholder);
        } else {
          // Si no hay más stakeholders en la lista, limpiamos los detalles
          this.clearStakeholderDetails();
        }
      }
    },
    clearStakeholderDetails() {
      this.name = '';
      this.specificities = '';
      this.requirements = '';
      this.generalDescription = '';
      this.relatedKPI = '';
    },
    viewStakeholderDetails(stakeholder) {
      this.selectedStakeholder = stakeholder.id;
      this.name = stakeholder.name;
      this.specificities = stakeholder.specificities;
      this.requirements = stakeholder.requirements;
      this.generalDescription = stakeholder.general_description;
      this.relatedKPI = stakeholder.related_kpi;
    },
    async saveChanges() {
      try {
        await this.saveStakeholder(); // Guarda los cambios del stakeholder actual
        await this.saveSelectedStakeholders(); // Guarda los IDs de los stakeholders seleccionados en problem_stakeholder
      } catch (error) {
        console.error('Error saving changes:', error);
      }
    },
    async saveStakeholder() {
      try {
        const apiUrl = this.selectedStakeholder ? `${this.apiUrl}/stakeholder/${this.selectedStakeholder}` : 'http://localhost:5000/stakeholder';
        const method = this.selectedStakeholder ? 'PUT' : 'POST';

        const response = await fetch(apiUrl, {
          method: method,
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            id: this.selectedStakeholder,
            selectedLab: this.selectedLab,
            name: this.name,
            specificities: 'Reviewed Stakeholder',
            requirements: this.requirements,
            general_description: this.generalDescription,
            related_kpi: this.relatedKPI,
            selectedProblem: this.selectedProblem,
            selectedStakeholders: this.selectedStakeholderList.map(stakeholder => stakeholder.id)
          })
        });
        const responseData = await response.json();

        if (!this.selectedStakeholder) {
          this.selectedStakeholder = responseData.id;
        }

        const updatedStakeholder = {
          id: this.selectedStakeholder,
          name: this.name,
          specificities: 'Reviewed Stakeholder',
          requirements: this.requirements,
          general_description: this.generalDescription,
          related_kpi: this.relatedKPI
        };

        const index = this.savedStakeholders.findIndex(item => item.id === this.selectedStakeholder);
        if (index !== -1) {
          this.savedStakeholders.splice(index, 1, updatedStakeholder);
        } else {
          this.savedStakeholders.push(updatedStakeholder);
        }

        const staticIndex = this.selectedStakeholderList.findIndex(item => item.id === this.selectedStakeholder);
        if (staticIndex !== -1) {
          this.selectedStakeholderList.splice(staticIndex, 1, updatedStakeholder);
        } else {
          this.selectedStakeholderList.push(updatedStakeholder);
        }

        this.fetchStakeholders();
        
        // Mostrar la notificación
        this.snackbar = true;
      } catch (error) {
        console.error('Error saving Stakeholder:', error);
      }
    },
    async saveSelectedStakeholders() {
      try {
        const response = await fetch(`${this.apiUrl}/save-stakeholders`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            selectedProblem: this.selectedProblem,
            selectedStakeholders: this.selectedStakeholderList.map(stakeholder => stakeholder.id)
          })
        });

        if (!response.ok) {
          console.error('Error saving selected stakeholders:', response.statusText);
        }
      } catch (error) {
        console.error('Error saving selected stakeholders:', error);
      }
    },

    async deleteGPTGeneratedStakeholders() {
      try {
        // Filtrar los IDs de los stakeholders generados por GPT-4o
        const gptGeneratedIds = this.stakeholders
          .filter(stakeholder => stakeholder.specificities === 'Stakeholder generated with GPT-4o')
          .map(stakeholder => stakeholder.id);

        // Eliminar cada stakeholder generado por GPT-4o
        for (const id of gptGeneratedIds) {
          await this.deleteStakeholderGenerated(id);
        }
      } catch (error) {
        console.error('Error deleting GPT generated stakeholders:', error);
      }
    },
  },
  watch: {
    selectedProblem(newProblemId, oldProblemId) {
      if (newProblemId !== oldProblemId) {
        this.deleteGPTGeneratedStakeholders()
        this.fetchStakeholders();
        
      }
    }
  },
  
  created() {
    this.deleteGPTGeneratedStakeholders();
    this.fetchStakeholders();
  }
};
</script>


<style scoped>
.stakeholder-selection {
  margin-top: 15px;
}
.v-btn.add {
  width: 100%;
  height: 40px; /* Ajusta según la altura del select */
  line-height: 40px; /* Centra el texto verticalmente */
  box-sizing: border-box;
  margin-bottom: 10px;
  margin-top: 10px;
  border: 2px solid rgb(44, 182, 125);
  background-color: transparent;
  color: rgb(44, 182, 125);
  font-size: 12px;
  cursor: pointer;

}


.v-btn.add:hover {
  background-color: rgb(44, 182, 125);
  color: white;
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
.temp-item {
  background-color:rgb(44, 182, 125) !important;
  font-weight: bold;
  color: white;

}
h3 {
 
  margin-bottom: 1rem;
  color: black;
}
.center-select-option {
  text-align: center;
}
</style>