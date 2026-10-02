<template>
    <v-card class="mx-auto" max-width="600" max-height="600">
        <div class="visual3d-wrapper">
      <input type="file" accept=".stl" @change="handleFileUpload" />
      <div id="canvasContainer">
        <TresCanvas v-bind="gl">
          <TresPerspectiveCamera :position="[3, 3, 3]" :fov="45" :look-at="[0, 0, 0]" />
          <OrbitControls />
          <TresAmbientLight :intensity="1" />
          <TresMesh v-if="stlGeometry" :geometry="stlGeometry">
            <TresMeshBasicMaterial color="black" />
          </TresMesh>
        </TresCanvas>
      </div>
    </div>
    </v-card>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { STLLoader } from 'three/examples/jsm/loaders/STLLoader';
  import { TresCanvas } from '@tresjs/core';
  import { OrbitControls } from '@tresjs/cientos';
  
  const gl = {
    clearColor: '#82DBC5',
    shadows: true,
    alpha: false,
  };
  
  const stlGeometry = ref(null);
  
  function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const loader = new STLLoader();
        const arrayBuffer = e.target.result;
        stlGeometry.value = loader.parse(arrayBuffer);
      };
      reader.readAsArrayBuffer(file);
    }
  }
  </script>
  
  <style>
  .visual3d-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    
  }
  
  #canvasContainer {
    width: 100%;
    max-width: 500px;
    height: 500px;
    margin-top: 20px;
    background-color: #000;
  }
  </style>
  