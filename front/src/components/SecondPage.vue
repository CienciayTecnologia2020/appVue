<template>
  <div class="container">
    <h1 class="text-box">Solution</h1>
    <h5 class="problem-title">Problem {{ selectedProblem }}</h5>
  </div>
</template>

<script>
export default ({
  props: ['selectedProblem']
})
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: flex-start; /* Alinea ambos títulos a la izquierda */
  height: 15vh; /* Ajusta la altura según tus necesidades */
}

.text-box {
  color: rgb(58, 59, 57);
  font-size: 36px;
  font-family: sans-serif;
  font-weight: bold; /* Aplica negrita a "Solution" */
  padding-left: 20px; /* Añade espacio a la izquierda si es necesario */
  margin-bottom: 10px; /* Espacio entre "Solution" y "Problem" */
}

.problem-title {
  font-size: 15px;
  padding-left: 20px; /* Alinea con el mismo espacio a la izquierda que "Solution" */
  color:rgb(116, 123, 130);
}
</style>
