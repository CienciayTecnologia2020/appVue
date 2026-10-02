<template>
  <v-container fluid>
    <v-row no-gutters>
      <v-col cols="5">
        <div class="h3">
          <h4>
            A model never perfectly reflects reality, which will result in a certain risk when you will take your final decision.
          </h4>
          <div>
            <h4>
              The risk you can accept must reflect:
            </h4>
            <li>
              the decision consequence
            </li>
            <li>
              the model influence on your decision
            </li>
          </div>   
          <h4>
            Make sure the model you choose does not exceed the risk you can accept.
          </h4>
        </div>
      </v-col>
      <v-col cols="7">
        <v-row class="center-y" no-gutters>
          <v-col cols="2">
            <div class="axis-y">Decision Consequence</div>
          </v-col>
          <v-col cols="10">
            <div class="square-container">
              <div class="square" @click="handleClick">
                <div class="diagonal"></div>
                <div class="selection" :style="{ top: mouseY + '%', left: mouseX + '%', width: selectionSize + 'px', height: selectionSize + 'px', borderRadius: (selectionSize / 2) + 'px' }"></div>
              </div>
            </div>
          </v-col>
          <v-col cols="6">
            <div class="axis-x">Model Influence</div>
            <div class="risk-display">Risk defined </div>
            <div class="risk-display">{{ risk }}</div>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
const apiUrl = process.env.VUE_APP_API_URL;
export default {
  props: ['selectedProblem'],
  data() {
    return {
      mouseX: 0,
      mouseY: 0,
      risk: '',
      selectionSize: 0,
      selectedEstimation: 'Quantitative',
      needData: null, // Almacena los datos de la respuesta del request
      selectedObjectives: [], // Almacena los objetivos seleccionados
      objectives: [] // Almacena los objetivos recibidos del servidor
    };
  },
  mounted() {
    this.fetchNeedData(); // Llama a la función para obtener los datos de necesidad
    this.fetchObjectives(); // Llama a la función para obtener los objetivos
  },
  watch: {
    needData: {
      immediate: true,
      handler(newValue) {
        if (newValue) {
          this.selectedEstimation = newValue.estimation_type;
          
          if (newValue.accepted_risk) {
            const mousePos = newValue.accepted_risk.split(',').map(coord => parseInt(coord.split(':')[1]));
            this.mouseX = mousePos[0];
            this.mouseY = mousePos[1];
          } else {
            this.mouseX = 0;
            this.mouseY = 0;
          }

          this.updateRisk();
          this.updateSelectionSize();

          // Actualiza los objetivos seleccionados
          if (newValue.objectives) {
            this.selectedObjectives = newValue.objectives.split(',').map(obj => obj.trim());
          } else {
            this.selectedObjectives = [];
          }
        }
      }
    },
    selectedEstimation: 'updateProblem',
    selectedObjectives: 'updateProblem',
    mouseX: 'updateProblem',
    mouseY: 'updateProblem'
  },
  methods: {
    // Función para obtener los datos de la necesidad
    async fetchNeedData() {
      try {
        const response = await fetch(`${apiUrl}/need/${this.selectedProblem}`); // Haz tu request
        const data = await response.json();
        this.needData = data[0]; // Asegúrate de acceder al primer objeto en el array
      } catch (error) {
        console.error('Error fetching need data:', error);
      }
    },
    // Función para obtener los objetivos desde el backend
    async fetchObjectives() {
      try {
        const response = await fetch(`${apiUrl}/objective`); // Haz tu request
        const data = await response.json();
        this.objectives = data; // Asigna los objetivos recibidos a la variable objectives
      } catch (error) {
        console.error('Error fetching objectives:', error);
      }
    },
    handleClick(event) {
      const rect = event.target.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;

      this.mouseX = Math.round((x / rect.width) * 100);
      this.mouseY = Math.round((y / rect.height) * 100);

      this.updateRisk();
      this.updateSelectionSize();
    },
    updateRisk() {
      this.risk = this.calculateRisk();
    },
    updateSelectionSize() {
      const squareContainer = this.$el.querySelector('.square-container');
      if (squareContainer) {
        const rect = squareContainer.getBoundingClientRect();
        this.selectionSize = rect.width * 0.1;
      }
    },
    calculateRisk() {
      const total = this.mouseX + (100 - this.mouseY);
      if (total <= 66) {
        return 'LOW';
      } else if (total <= 132) {
        return 'MEDIUM';
      } else {
        return 'HIGH';
      }
    },
    // Nueva función para actualizar el problema
    async updateProblem() {
      try {
        const updateData = {
          estimation_type: this.selectedEstimation,
          accepted_risk: `mouseX: ${this.mouseX}, mouseY: ${this.mouseY}`,
          objectives: this.selectedObjectives.join(', '),
        };

        const response = await fetch(`${apiUrl}/need/${this.selectedProblem}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(updateData),
        });

        if (response.ok) {
          console.log('Problem updated successfully');
        } else {
          console.error('Failed to update the problem');
        }
      } catch (error) {
        console.error('Error updating the problem:', error);
      }
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.h3 {
  margin-top: 50px;
  text-align: left;
  line-height: 1.5; /* Ajusta el espaciado entre líneas */
}

.h3 h4, .h3 li {
  margin-bottom: 10px; /* Espacio de 5px entre elementos */
}


.checklist {
  margin-right: 20px;
}

.square-container {
  width: 400px;
  height: 400px;
  position: relative;
  background-color: #f3f3f3;
  border-radius: 5px;
  overflow: hidden;
}

.square {
  width: 100%;
  height: 100%;
  position: relative;
}

.diagonal {
  width: 100%;
  height: 100%;
  position: absolute;
  background: linear-gradient(to bottom left, rgba(248, 244, 3, 0.92), transparent);
}

.selection {
  position: absolute;
  background-color: rgba(5, 21, 8, 0.3);
  z-index: 1;
}

.axis-x {
  width: 100%;
  height: 20px;
  line-height: 20px;
  text-align: center;
  font-size: 12px;
  font-weight: bold;
}

.axis-y {
  width: 100%;
  text-align: center;
  transform: translateY(-50%) rotate(-90deg);
  font-size: 12px;
  font-weight: bold;
}

.risk-display {
  width: 100%;
  text-align: center;
  margin-top: 10px;
  font-size: 18px;
  font-weight: bold;
  color: #00a000;
}

.center-y {
  align-items: center;
}
</style>

