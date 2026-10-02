<template>
  <div class="lab-container">
    <select v-model="tempSelectedLab" @change="handleLabSelection" class="lab-select">
      <option :value="null" disabled selected>Select a Location</option>
      <option v-for="lab in labs" :value="lab.id" :key="lab.id">{{ lab.name }}</option>
    </select>
    <div v-if="labInfo" class="lab-info">
      <h2>{{ labInfo.name }}</h2>
      <div class="lab-details">
        <div class="lab-description">
          <p>{{ labInfo.description }}</p>
        </div>
        <div class="lab-image-container">
          <img :src="labInfo.image" alt="Lab Image" class="lab-image">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const apiUrl = process.env.VUE_APP_API_URL;
import axios from 'axios';

export default {
  props: ['selectedProblem'],
  data() {
    return {
      selectedLab: null,
      tempSelectedLab: null,
      labs: [],
      labInfo: null
    };
  },
  watch: {
    selectedProblem(newVal, oldVal) {
      if (newVal !== oldVal) {
        this.fetchLabs();
      }
    },
    tempSelectedLab(newVal, oldVal) {
      if (newVal !== oldVal) {
        console.log('tempSelectedLab:', newVal);
      }
    }
  },
  created() {
    this.fetchLabs();
  },
  methods: {
    async fetchLabs() {
      if (this.selectedProblem) {
        try {
          const response = await axios.get(`${apiUrl}/labs`, {
            params: {
              selectedProblem: this.selectedProblem
            }
          });
          this.labs = response.data;
          console.log('Labs:', this.labs);
          if (this.labs.length > 0) {
            this.selectedLab = this.labs[0].id; // Seleccionar el primer laboratorio por defecto
            this.fetchLabData(); // Cargar datos del laboratorio predeterminado
          }
        } catch (error) {
          console.error('Error fetching labs:', error);
        }
      }
    },
    async fetchLabData() {
      if (this.selectedLab) {
        try {
          this.labInfo = null;
          const response = await axios.post(`${apiUrl}/lab_data`, { 
            selectedProblem: this.selectedProblem,
            selectedLab: this.selectedLab
          });
          this.labInfo = response.data[0]; // Tomamos el primer elemento de la lista de lab_info
          
        } catch (error) {
          console.error('Error fetching lab data:', error);
        }
      }
    },
    async handleLabSelection() {
      this.selectedLab = this.tempSelectedLab;
      this.tempSelectedLab = null;  // Reset the tempSelectedLab to null
      await this.updateProblemContext();
      this.fetchLabData();
    },
    async updateProblemContext() {
      try {
        const response = await axios.post(`${apiUrl}/update_problem_location`, {
          problem_id: this.selectedProblem,
          context_id: this.selectedLab,
          
        });
        this.$emit('selectedLab', this.selectedLab);
        
        if (response.data.error) {
          throw new Error(response.data.error);
        } else {
          console.log('Problem context updated successfully');
          this.fetchLabData(); // Refrescar los datos del lab después de actualizar el contexto
        }
      } catch (error) {
        console.error('Error updating problem context:', error);
      }
    }
  }
};
</script>

<style scoped>
.lab-container {
  
  min-width: 500px;
  margin: auto;
  min-height: 500px;
}

.lab-select {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #ccc;
  margin-bottom: 20px;
}

.lab-info {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}

.lab-info h2 {
  width: 100%;
  margin-bottom: 20px;
}

.lab-details {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.lab-description {
  flex: 1;
  margin-right: 20px;
  text-align: left;
}

.lab-image-container {
  max-width: 200px;
  flex-shrink: 0;
}

.lab-image {
  width: 100%;
  max-width: 100%;
  height: auto;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>