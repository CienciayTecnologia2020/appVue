<template>
  <div id="app">
    <!-- Aquí podrías incluir un encabezado común, una barra de navegación, etc. -->
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
}
.nav-container {
  top: 0;
  position: sticky;
  z-index: 1000;
  background-color: white;
}

.DecisionPorpuse {
  display: flex;
  justify-content: space-between;
  width: flex; /* Ancho fijo de los componentes */
  margin: 0 auto; /* Centra los componentes horizontalmente */
  top: 0;
  background-color: white; /* Fondo blanco para cubrir los componentes que se muevan detrás */
  z-index: 1000; /* Asegura que estén por encima de otros elementos */
  /* border: 1px solid #ccc; Añade un borde de 1px sólido con color gris claro */
  border-radius: 5px; /* Añade bordes redondeados */
  margin-bottom: 20px;
}

/* Estilos para las tarjetas de sección */
.section-card {
  margin-bottom: 20px; /* Espacio entre tarjetas */

}

.title {
  text-align: left; /* Alineación del texto a la izquierda */
  font-size: 18px; /* Tamaño del texto */
  font-weight: bold; /* Texto en negrita */
  color: rgb(251, 252, 250);/* Color del texto */
  background-color: rgb(44, 182, 125);
}
</style>