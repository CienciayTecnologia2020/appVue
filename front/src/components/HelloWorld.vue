<template>
  <div class="container">

    <div class="text-container">
      <h3>{{ message }}</h3>
      <h6>Powered by MIC</h6>
    </div>
    <div class="image-container">
      <div class="image-container">
      <v-img
        class="image"
        :width= "100"
        aspect-ratio="4/3"
        cover
        src="https://smartinnovationnorway.com/wp-content/uploads/2021/12/ProBono-1024x425-1.png"
      ></v-img>
    </div>
    </div>

  </div>
</template>

<script>

export default {
  data() {
    return {
      message: 'Decision Workflow',

    };
  }
};
</script>

<style>
.container {
  display: flex;
}

.text-container {
  flex: 1; /* El texto ocupará todo el espacio disponible */
  text-align: left;
  margin-left: 10px;
}

h3 {
  color: rgb(44, 182, 125);
}

.image-container {
  margin-left: 20px; /* Espacio entre el texto y la imagen */
}

.image {
  width: 100%; /* Asegura que la imagen ocupe todo el ancho disponible en su contenedor */
}
</style>

