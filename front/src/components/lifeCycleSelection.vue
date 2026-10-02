<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card-title class="fixed-label">
          <!--<h3>Selected KPI ID: {{ selectedKPI }}</h3>-->
        </v-card-title>

        <!-- Menú desplegable para seleccionar lifecycle -->
        <div>
          <select v-model="selectedLifeCycle" @change="addLifeCycle" class="custom-select">
            <option :value="null" disabled>Select a Life Cycle</option>
            <option v-for="lifecycle in lifeCycles" :value="lifecycle.id" :key="lifecycle.id">{{ lifecycle.name }}</option>
          </select>
        </div>

        <!-- Tags de Life Cycles seleccionados -->
        <div class="tags">
          <span v-for="(lifecycle, index) in selectedLifeCycles" :key="index" class="tag">
            {{ lifecycle.name }}
            <button @click="removeLifeCycle(lifecycle.id)" class="remove-tag">x</button>
          </span>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
const apiUrl = process.env.VUE_APP_API_URL;

export default {
  props: ['selectedKPI'],
  data() {
    return {
      lifeCycles: [],
      selectedLifeCycle: null, // Default value should be null to match the default option
      selectedLifeCycles: []
    };
  },
  created() {
    this.fetchLifeCycles();
    this.fetchSelectedLifeCycles();
  },
  watch: {
    selectedKPI() {
      this.fetchSelectedLifeCycles();
    }
  },
  methods: {
    async fetchLifeCycles() {
      try {
        const response = await fetch(`${apiUrl}/lifecycle`);
        const data = await response.json();
        this.lifeCycles = data;
      } catch (error) {
        console.error('Error fetching lifeCycles:', error);
      }
    },
    async fetchSelectedLifeCycles() {
      if (!this.selectedKPI) return;
      try {
        const response = await fetch(`${apiUrl}/lifecycle-kpi/${this.selectedKPI}`);
        const data = await response.json();
        // Asegúrate de que `data` tenga objetos con id y name
        this.selectedLifeCycles = data.map(item => ({ id: item.id, name: item.name }));
      } catch (error) {
        console.error('Error fetching selected lifeCycles:', error);
      }
    },
    async addLifeCycle() {
      if (this.selectedKPI && this.selectedLifeCycle) {
        // Verificar si el lifecycle ya está en la lista seleccionada
        const existingLifeCycle = this.selectedLifeCycles.find(lc => lc.id === this.selectedLifeCycle);
        if (existingLifeCycle) {
          console.log('Lifecycle already selected');
          return;
        }

        try {
          const response = await fetch(`${apiUrl}/lifecycle/${this.selectedKPI}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ lifecycle_id: this.selectedLifeCycle })
          });
          if (!response.ok) {
            console.error('Error updating lifecycle:', response.statusText);
          } else {
            const lifecycle = this.lifeCycles.find(lc => lc.id === this.selectedLifeCycle);
            if (lifecycle) {
              this.selectedLifeCycles.push({ id: lifecycle.id, name: lifecycle.name });
            }
            this.selectedLifeCycle = null; // Reset the selected life cycle
          }
        } catch (error) {
          console.error('Error updating lifecycle:', error);
        }
      }
    },
    async removeLifeCycle(lifeCycleId) {
      try {
        const response = await fetch(`${apiUrl}/lifecycle/${this.selectedKPI}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ lifecycle_id: lifeCycleId })
        });
        if (!response.ok) {
          console.error('Error deleting lifecycle:', response.statusText);
        } else {
          this.selectedLifeCycles = this.selectedLifeCycles.filter(lc => lc.id !== lifeCycleId);
        }
      } catch (error) {
        console.error('Error deleting lifecycle:', error);
      }
    }
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
}

.custom-select:focus {
  border-color: #50ff76;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(1, 20, 8, 0.25);
}

.fixed-label {
  font-weight: bold;
}

.tags {
  margin-top: 1rem;
}

.tag {
  display: inline-block;
  background-color: #e0e0e0;
  border-radius: 0.25rem;
  padding: 0.25rem 0.5rem;
  margin: 0.25rem;
}

.remove-tag {
  background: none;
  border: none;
  margin-left: 0.5rem;
  cursor: pointer;
}
</style>
