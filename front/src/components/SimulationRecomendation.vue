<template>
  <div>
    <v-btn @click="fetchRecommendations" :disabled="isLoading">
      <v-icon v-if="isLoading" left>mdi-loading mdi-spin</v-icon>
      <span v-if="isLoading">Loading...</span>
      <span v-else>Generate More Recommendations</span>
    </v-btn>

    <v-row v-if="tools.length" class="my-4">
      <v-col cols="12">
        <v-row justify="center" class="cards-container">
          <v-col v-for="(tool, index) in tools" :key="index" cols="12" sm="6" md="4" lg="3">
            <v-card class="pa-3 mb-3 tool-card">
              <v-card-title class="multiline-text"><strong>{{ tool.name }}</strong></v-card-title>
              <v-card-text class="multiline-text">{{ tool.explanation }}</v-card-text>
              <v-card-text class="multiline-text">
                <a :href="tool.url" target="_blank" rel="noopener noreferrer">{{ tool.url }}</a>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <p v-else></p>
  </div>
</template>
<script>
const apiUrl = process.env.VUE_APP_API_URL;
export default {
  props: ['selectedLab', 'selectedProblem'],
  data() {
    return {
      tools: [],
      isLoading: false
    };
  },
  methods: {
    async fetchRecommendations() {
      this.isLoading = true; // Mostrar icono de carga
      try {
        const response = await fetch(`${apiUrl}/gpt-recomendation`, {
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
          const data = await response.json();
          this.tools = data;
          this.$nextTick(() => {
            this.setMaxHeight();
          });
        } else {
          console.error('Error fetching recommendations:', response.statusText);
        }
      } catch (error) {
        console.error('Error fetching recommendations:', error);
      } finally {
        this.isLoading = false; // Ocultar icono de carga
      }
    },
    setMaxHeight() {
      // No need for JavaScript adjustments with flexbox solution
    }
  }
};
</script>
<style scoped>
h2 {
  color: #333;
}
button {
  margin-top: 20px;
  border: 2px solid rgb(44, 182, 125);
  background-color: transparent;
  color: rgb(44, 182, 125);
  font-size: 12px;
  cursor: pointer;
  border-radius: 5px;
  margin-bottom: 20px;
  width: 300px;
}

button:hover {
  background-color: rgb(44, 182, 125);
  color: white;
}
.multiline-text {
  white-space: pre-wrap; /* Permite el ajuste de línea y preserva los saltos de línea */
  word-wrap: break-word; /* Permite la división de palabras largas */
  overflow: visible; /* Asegura que todo el contenido se muestre */
  text-overflow: unset; /* Elimina los puntos suspensivos en el desbordamiento de texto */
  /* text-align: justify;  Justifica el texto */
}
a {
  color: #1e88e5; /* Color del enlace */
  text-decoration: none; /* Elimina el subrayado por defecto */
}
a:hover {
  text-decoration: underline; /* Subraya el enlace al pasar el mouse */
}
.cards-container {
  display: flex;
  flex-wrap: wrap;
}
.tool-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}
.v-card {
  display: flex;
  flex-direction: column;
  height: 100%;
}
</style>
