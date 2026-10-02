<template>
  <div>
    <!-- Usamos la clase "d-flex" para flexbox y "flex-column" para apilar los botones verticalmente -->
    <div class="d-flex flex-column">
      <v-btn :text="true" @click="scrollToSection('app')" :class="{ 'selected': selectedSection === 'app' }">
        <span class="small-text font-weight-bold">Solution</span>
      </v-btn>
      <v-btn :text="true" @click="scrollToSection('2-Building or Neighborhood')" :class="{ 'selected': selectedSection === '2-Building or Neighborhood' }">
        <span class="small-text font-weight-bold">Scenarios</span>
      </v-btn>
      <v-btn :text="true" @click="scrollToSection('3-Design Space')" :class="{ 'selected': selectedSection === '3-Design Space' }">
        <span class="small-text font-weight-bold">Requirements</span>
      </v-btn>
      <v-btn :text="true" @click="scrollToSection('1-Decision Purpose')" :class="{ 'selected': selectedSection === '1-Decision Purpose' }">
        <span class="small-text font-weight-bold">Accepted Model Risk</span>
      </v-btn>
      <v-btn :text="true" @click="scrollToSection('6-Simulation Tools')" :class="{ 'selected': selectedSection === '6-Simulation Tools' }">
        <span class="small-text font-weight-bold">Simulation Tools</span>
      </v-btn>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NavigationBar',
  data() {
    return {
      selectedSection: '' // Variable para almacenar la sección seleccionada
    };
  },
  methods: {
    scrollToSection(sectionId) {
      const section = document.getElementById(sectionId);
      if (section) {
        if (sectionId === 'app') {
          window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
          section.scrollIntoView({ behavior: 'smooth' });
        }
        this.selectedSection = sectionId; // Actualiza la sección seleccionada
      }
    },
    onScroll() {
      clearTimeout(this.scrollTimeout);
      this.scrollTimeout = setTimeout(() => {
        const sections = ['app', '2-Building or Neighborhood', '3-Design Space', '1-Decision Purpose', '6-Simulation Tools'];
        let currentSection = '';
        sections.forEach(sectionId => {
          const section = document.getElementById(sectionId);
          const rect = section.getBoundingClientRect();
          if (rect.top <= 50 && rect.bottom >= 50) {
            currentSection = sectionId;
          }
        });
        this.selectedSection = currentSection;
      }, 100); // Retraso de 100ms para asegurar un desplazamiento suave
    }
  },
  mounted() {
    window.addEventListener('scroll', this.onScroll);
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.onScroll);
  }
};
</script>

<style scoped>
/* Estilos específicos de la barra de navegación */
/* Estilo general para los botones */
.small-text {
  font-size: 10px; /* Tamaño de fuente más pequeño */
}

.font-weight-bold {
  font-weight: bold; /* Texto en negrita */
}

/* Estilo para el primer botón */
.d-flex .v-btn:first-child {
  background-color: rgb(44, 182, 125); /* Color de fondo gris */
  color: #2cb67d; /* Texto verde */
  width: 140%; /* Ancho ligeramente mayor que los otros botones */
  margin-bottom: 8px; /* Espacio inferior para separar del siguiente botón */
}

.d-flex .v-btn:first-child .small-text {
  color: black; /* Asegura que el texto dentro del span también sea verde */
}

/* Estilo cuando el botón está seleccionado */
.selected {
  background-color: rgb(44, 182, 125); /* Color de fondo verde cuando el botón está seleccionado */
  color: white; /* Texto blanco cuando el botón está seleccionado */
}
</style>
