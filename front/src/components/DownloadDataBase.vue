<template>
    <v-container>
      <v-row>
        <v-col>
          <v-btn outlined color="blue" @click="downloadDbStructure" :disabled="isLoading">
            <v-icon v-if="isLoading">mdi-loading mdi-spin</v-icon>
            <span v-else>Download Problem Information</span>
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  const apiUrl = process.env.VUE_APP_API_URL;
  import axios from 'axios';
  
  export default {
    props: ['selectedProblem'],
    data() {
      return {
        isLoading: false
      };
    },
    methods: {
      async downloadDbStructure() {
        try {
          this.isLoading = true;
  
          // Hacer la solicitud GET con el problema seleccionado
          const response = await axios.get(`${apiUrl}/download-db-structure/${this.selectedProblem}`);
          const dbStructure = response.data;
  
          // Convertir a JSON y crear un archivo para descargar
          const blob = new Blob([JSON.stringify(dbStructure, null, 2)], { type: 'application/json' });
          const url = URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', 'db_structure.json');
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
  
          this.isLoading = false;
        } catch (error) {
          console.error('Error downloading DB structure:', error);
          alert('Failed to download DB structure.');
          this.isLoading = false;
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .v-btn {
    margin-top: 20px;
  }
  </style>
  
  