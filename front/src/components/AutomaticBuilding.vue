<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card-title class="fixed-label"></v-card-title>

        <!-- Lista de Buildings guardados -->
        <v-row v-if="savedBuildings.length > 0">
          <!-- Aquí podrías agregar un componente para mostrar los savedBuildings -->
        </v-row>
      </v-col>

      <v-col cols="4">
        <!-- Lista estática de Buildings seleccionados -->
        <!-- Menú desplegable para seleccionar Buildings -->
        <div class="building-selection">
          <!-- Botones de crear nuevo y guardar cambios -->
          <v-btn @click="createNewBuilding" class="create-new">CREATE NEW</v-btn>
          <select v-model="selectedBuilding" @change="selectBuilding" class="custom-select">
            <option :value="null" disabled class="center-select-option">Select a Building</option>
            <option v-for="building in buildings" :value="building.id" :key="building.id">{{ building.name }}</option>
          </select>
        </div>
        <v-list v-if="selectedBuildingList.length > 0">
          <h3>Selected Buildings</h3>
          <v-list-item
            v-for="building in selectedBuildingList"
            :key="building.id"
            @click="viewBuildingDetails(building)"
            :class="{ 'selected': building.id === selectedBuilding || building.temp }"
          >
            <v-list-item-content>
              <v-list-item-title>{{ building.name }}</v-list-item-title>
              <v-list-item-subtitle>Description: {{ building.description }}</v-list-item-subtitle>
              <v-list-item-subtitle>Address: {{ building.address }}</v-list-item-subtitle>
            </v-list-item-content>
            <!-- Botón de eliminar -->
            <v-icon @click.stop="removeFromSelectedBuildingList(building.id)" color="red">mdi-close-circle</v-icon>
          </v-list-item>
        </v-list>
      </v-col>

      <v-col cols="8">
        <v-card-title class="fixed-label">
          <span>Building Information</span>
                            <!-- Componente Visual3D en lugar de FileName -->
          
        </v-card-title>

        <!-- Mostrar las características del Building seleccionado -->
        <div>
          <v-text-field v-model="name" label="Name"></v-text-field>
          <v-text-field v-model="description" label="Description" class="wider-description"></v-text-field>
          <v-text-field v-model="address" label="Address"></v-text-field>
          <v-text-field v-model="gps" label="GPS Coord"></v-text-field>
          
          <Visual3D />
         
       


          <!-- Botón de eliminar -->
          <v-btn v-if="selectedBuilding" @click.stop="confirmDeleteBuilding(selectedBuilding)" color="red">Delete</v-btn>
        </div>
        <div>
          <v-btn @click="saveBuilding" color="yellow" block class="mt-4">Save Changes</v-btn>
        </div>
      </v-col>
    </v-row>

    <!-- Diálogo de confirmación -->
    <v-dialog v-model="confirmDialog" max-width="400">
      <v-card>
        <v-card-title>Confirm Delete</v-card-title>
        <v-card-text>Are you sure you want to delete this Building?</v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="deleteBuilding">Yes</v-btn>
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


const apiUrl = process.env.VUE_APP_API_URL;

export default {
  
  props: ['selectedLab', 'selectedProblem'],

  data() {
    return {
      apiUrl: process.env.VUE_APP_API_URL,
      name: '',
      description: '',
      address: '',
      gps: '',
      filename: '',
      date: '',
      version: '',
      selectedBuilding: null,
      selectedBuildingList: [],
      buildings: [],
      savedBuildings: [],
      confirmDialog: false,
      buildingToDelete: null,
      snackbar: false,
      snackbarTimeout: 3000,
      scene: null,
      camera: null,
      renderer: null,
      stlMesh: null,
    };
  },
  methods: {

    confirmDeleteBuilding(buildingId) {
      this.buildingToDelete = buildingId;
      this.confirmDialog = true;
    },
    async deleteBuilding() {
      try {
        const response = await fetch(`${apiUrl}/building/${this.buildingToDelete}`, {
          method: 'DELETE'
        });
        if (response.ok) {
          this.removeFromSelectedBuildingList(this.buildingToDelete);
          this.confirmDialog = false;
          this.snackbar = true;
          this.fetchBuildings();
        } else {
          console.error('Error deleting Building:', response.statusText);
        }
      } catch (error) {
        console.error('Error deleting Building:', error);
      }
    },
    async createNewBuilding() {
  // Limpiar los detalles del edificio
  this.clearBuildingDetails();
  // Crear un nuevo edificio temporal en la lista estática
  const newTempBuilding = {
    id: 'temp-' + new Date().getTime(),
    name: 'New Building',
    description: '',
    address: '',
    gps: '',
    filename: '',
    date: '',
    version: '',
    temp: true
  };
  // Agregar el nuevo edificio temporal a la lista de edificios seleccionados
  this.selectedBuildingList.push(newTempBuilding);
  // Ver los detalles del nuevo edificio temporal
  this.viewBuildingDetails(newTempBuilding);

  // Enviar una solicitud POST al servidor para crear el nuevo edificio
  try {
    const response = await fetch(`${apiUrl}/building`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: newTempBuilding.name,
        description: newTempBuilding.description,
        address: newTempBuilding.address,
        gps: newTempBuilding.gps,
        filename: newTempBuilding.filename,
        date: newTempBuilding.date,
        version: newTempBuilding.version,
        selectedProblem: this.selectedProblem,
        selectedLab: this.selectedLab
      })
    });

    if (response.ok) {
      // Recibir el edificio creado desde el servidor
      const createdBuilding = await response.json();
      // Actualizar el id del edificio temporal con el id recibido del servidor
      newTempBuilding.id = createdBuilding.id;

      // Eliminar el atributo temporal del edificio una vez que se ha creado en el servidor
      delete newTempBuilding.temp;

      // Actualizar la lista de edificios después de crear el nuevo edificio
      this.fetchBuildings();

      // Seleccionar el nuevo edificio creado
      this.selectedBuilding = newTempBuilding.id;
    } else {
      console.error('Error creating new building:', response.statusText);
    }
  } catch (error) {
    console.error('Error creating new building:', error);
  }
}
,
    async fetchBuildings() {
      if (this.selectedLab) {
        try {
          const response = await fetch(`${apiUrl}/building/${this.selectedLab}?selectedProblem=${this.selectedProblem}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json'
            },
          });
          const data = await response.json();
          this.buildings = data;
          this.selectedBuildingList = this.buildings.filter(building => building.selectedBuilding);
        } catch (error) {
          console.error('Error fetching Buildings:', error);
          this.buildings = [];
        }
      }
    },
    async selectBuilding() {
      if (this.selectedBuilding) {
        const selectedBuildingData = this.buildings.find(building => building.id === this.selectedBuilding);
        if (selectedBuildingData) {
          this.viewBuildingDetails(selectedBuildingData);
          this.addToSelectedBuildingList(selectedBuildingData);
        }
      }
    },
    async addToSelectedBuildingList(building) {
      if (!this.selectedBuildingList.find(item => item.id === building.id)) {
        this.selectedBuildingList.push(building);
        try {
          const response = await fetch(`${apiUrl}/add-building/${building.id}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ selectedProblem: this.selectedProblem })
          });
          if (!response.ok) {
            console.error('Error adding building to list:', response.statusText);
          }
        } catch (error) {
          console.error('Error adding building to list:', error);
        }
      }
    },
    async removeFromSelectedBuildingList(buildingId) {
      const index = this.selectedBuildingList.findIndex(item => item.id === buildingId);
      if (index !== -1) {
        this.selectedBuildingList.splice(index, 1);
        try {
          const response = await fetch(`${apiUrl}/delete-building/${buildingId}`, {
            method: 'DELETE'
          });
          if (!response.ok) {
            console.error('Error removing building from list:', response.statusText);
          }
        } catch (error) {
          console.error('Error removing building from list:', error);
        }
        if (this.selectedBuilding === buildingId) {
          const previousIndex = index > 0 ? index - 1 : null;
          this.selectedBuilding = previousIndex !== null ? this.selectedBuildingList[previousIndex].id : null;
          if (this.selectedBuilding) {
            this.viewBuildingDetails(this.selectedBuildingList[previousIndex]);
          } else {
            this.clearBuildingDetails();
          }
        }
      }
      // Si no hay ningún building seleccionado después de la eliminación, seleccionamos el último building restante
      if (!this.selectedBuilding && this.selectedBuildingList.length > 0) {
        this.selectedBuilding = this.selectedBuildingList[this.selectedBuildingList.length - 1].id;
        this.viewBuildingDetails(this.selectedBuildingList[this.selectedBuildingList.length - 1]);
      }
    },
    viewBuildingDetails(building) {
      this.selectedBuilding = building.id;
      this.name = building.name;
      this.description = building.description;
      this.address = building.address;
      this.gps = building.gps;
      this.filename = building.filename;
      this.date = building.date;
      this.version = building.version;
    },
    clearBuildingDetails() {
      this.name = '';
      this.description = '';
      this.address = '';
      this.gps = '';
      this.filename = '';
      this.date = '';
      this.version = '';
    },
    async saveBuilding() {
      try {
        console.log
        const apiUrl = this.selectedBuilding ? `${this.apiUrl}/building/${this.selectedBuilding}` : `${this.apiUrl}/building`;
        const method = this.selectedBuilding ? 'PUT' : 'POST';

        const response = await fetch(apiUrl, {
          method: method,
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: this.name,
            description: this.description,
            address: this.address,
            gps: this.gps,
            selectedProblem: this.selectedProblem
          })
        });
        this.fetchBuildings();
        if (response.ok) {
          this.snackbar = true;
          const savedBuilding = await response.json();
          
          if (!this.selectedBuilding || this.selectedBuilding.startsWith('temp-')) {
            this.buildings.push(savedBuilding);
            this.selectedBuilding = savedBuilding.id;
            this.addToSelectedBuildingList(savedBuilding);
          } else {
            const index = this.buildings.findIndex(building => building.id === this.selectedBuilding);
            if (index !== -1) {
              this.buildings.splice(index, 1, savedBuilding);
              const selectedIndex = this.selectedBuildingList.findIndex(building => building.id === this.selectedBuilding);
              if (selectedIndex !== -1) {
                this.selectedBuildingList.splice(selectedIndex, 1, savedBuilding);
              }
            }
          }
        } else {
          console.error('Error saving building:', response.statusText);
        }
      } catch (error) {
        console.error('Error saving building:', error);
      }
    }
  }
  ,
  watch: {
    selectedLab() {
      this.fetchBuildings();
    },
    selectedProblem() {
      this.fetchBuildings();
    }
  },
  created() {
    this.fetchBuildings();
    
  },
  mounted() {
  this.fetchBuildings();

}

  
};
</script>



<style scoped>
.custom-select {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #c0e8c6;
  border-radius: 0.25rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  height: 40px; /* Ajusta según la altura del botón */
  box-sizing: border-box; /* Asegura que el padding no afecte el tamaño total */
}

.custom-select:focus {
  border-color: #50ff76;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(1, 20, 8, 0.25);
}

.v-btn.create-new {
  width: 100%;
  height: 40px; /* Ajusta según la altura del select */
  line-height: 40px; /* Centra el texto verticalmente */
  box-sizing: border-box;
  margin-bottom: 10px;
  border: 2px solid rgb(44, 182, 125);
  background-color: transparent;
  color: rgb(44, 182, 125);
  font-size: 12px;
  cursor: pointer;

}


.v-btn.create-new:hover {
  background-color: rgb(44, 182, 125);
  color: white;
}

.building-selection {
  display: flex;
  flex-direction: column;
  gap: 10px; /* Espacio entre el botón y el select */
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

#stlViewer {
  width: 100%;
  height: 500px;
}
h3 {
  
  
  margin-bottom: 1rem;
  color: black;
}
.center-select-option {
  text-align: center;
}
</style>
