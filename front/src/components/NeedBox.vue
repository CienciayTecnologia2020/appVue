<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card-title class="fixed-label">
          <!-- Título u otro contenido -->
        </v-card-title>
        <!-- Cuadro de texto para actualizar el need -->
        <v-textarea
          v-model="need"
          label="Write the current need or pain"
          rows="5"
          outlined
          @blur="updateNeed" 
        ></v-textarea>
      </v-col>
    </v-row>
    <!-- Notificación de éxito -->
    <v-snackbar v-model="snackbar" :timeout="snackbarTimeout" color="success">
      Need updated successfully!
      <v-btn text @click="snackbar = false">Close</v-btn>
    </v-snackbar>
  </v-container>
</template>

<script>

const apiUrl = process.env.VUE_APP_API_URL;
export default {
  props: ['selectedProblem'],
  data() {
    return {
      needs: [],
      need: '',
      snackbar: false,
      snackbarTimeout: 3000
    };
  },
  methods: {
    async fetchNeed() {
      if (this.selectedProblem) {
        try {
          const response = await fetch(`${apiUrl}/need/${this.selectedProblem}`);
          const data = await response.json();
          this.needs = data;
          this.need = data.length > 0 ? data[0].need : '';
        } catch (error) {
          console.error('Error fetching needs:', error);
        }
      } else {
        console.warn('No problem selected');
      }
    },
    async updateNeed() {
      if (this.selectedProblem) {
        try {
          const response = await fetch(`${apiUrl}/update_need/${this.selectedProblem}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ need: this.need })
          });
          const result = await response.json();
          if (response.ok) {
            this.snackbar = true;
          } else {
            console.error('Error updating need:', result.error);
          }
        } catch (error) {
          console.error('Error updating need:', error);
        }
      } else {
        console.warn('No problem selected');
      }
    }
  },
  watch: {
    selectedProblem: {
      immediate: true,
      handler() {
        this.fetchNeed();
      }
    }
  }
};
</script>

<style scoped>
.fixed-label {
  font-weight: bold;
}
</style>
