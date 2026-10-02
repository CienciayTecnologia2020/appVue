<template>
  <div>
    <!-- Botón Add para mostrar/ocultar el formulario de agregar -->
    <button @click="toggleAddForm" class="add-button">Add</button>
    
    <!-- Lista de requisitos -->
    <div class="container">
      <ul class="requirements-list">
        <li v-for="requirement in requirements" :key="requirement.id">
          <strong>{{ requirement.attribute }}</strong>
          <span 
            v-if="!requirement.editing"
            @click="startEditing(requirement)"
            class="editable-text"
          >{{ requirement.text }}</span>
          <input 
            v-else 
            type="text" 
            v-model="requirement.text" 
            @blur="saveRequirement(requirement)" 
            class="edit-input"
          >
          <span v-if="requirement.editing" class="save-indicator">(Saved)</span>
          <span class="delete-button" @click="deleteRequirement(requirement.id)">❌</span>
        </li>
      </ul>
    </div>

    <!-- Formulario para agregar un nuevo requisito -->
    <div v-if="showAddForm" class="add-requirement">
      <h3>Add Requirement</h3>
      <label for="attributeSelect">Attribute:</label>
      <select id="attributeSelect" v-model="selectedAttribute">
        <option v-for="attribute in attributes" :key="attribute.id" :value="attribute.id">{{ attribute.name }}</option>
      </select>
      <br>
      <label for="requirementText">Text:</label>
      <input type="text" id="requirementText" v-model="newRequirementText">
      <br>
      <button @click="saveNewRequirement">Save</button>
      <button @click="toggleAddForm">Cancel</button>
    </div>
  </div>
</template>

<script>
const apiUrl = process.env.VUE_APP_API_URL;
export default {
  props: ['selectedProblem'],
  data() {
    return {
      requirements: [],
      attributes: [], // Lista de atributos
      selectedAttribute: null, // Atributo seleccionado en el formulario
      newRequirementText: '', // Texto del nuevo requisito a agregar
      showAddForm: false // Mostrar u ocultar el formulario de agregar
    };
  },
  mounted() {
    this.fetchRequirements();
    this.fetchAttributes(); // Cargar lista de atributos al montar el componente
  },
  methods: {
    fetchRequirements() {
      fetch(`${apiUrl}/test/${this.selectedProblem}`)
        .then(response => response.json())
        .then(data => {
          this.requirements = data.map(req => ({ ...req, editing: false }));
        })
        .catch(error => {
          console.error('Error fetching requirements:', error);
        });
    },
    fetchAttributes() {
      fetch(`${apiUrl}/attribute`)
        .then(response => response.json())
        .then(data => {
          this.attributes = data;
        })
        .catch(error => {
          console.error('Error fetching attributes:', error);
        });
    },
    toggleAddForm() {
      this.showAddForm = !this.showAddForm;
      if (!this.showAddForm) {
        this.clearForm();
      }
    },
    saveNewRequirement() {
      const newRequirement = {
        attribute_id: this.selectedAttribute,
        text: this.newRequirementText,
        problem_id: this.selectedProblem
      };

      fetch(`${apiUrl}/test`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newRequirement)
      })
      .then(response => {
        if (response.ok) {
          this.fetchRequirements(); // Refrescar la lista después de agregar
          this.toggleAddForm(); // Ocultar formulario después de agregar
        } else {
          console.error('Failed to add requirement');
        }
      })
      .catch(error => {
        console.error('Error adding requirement:', error);
      });
    },
    saveRequirement(requirement) {
      fetch(`${apiUrl}/test/${requirement.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          attribute_id: requirement.attribute_id,
          text: requirement.text,
          problem_id: this.selectedProblem
        })
      })
      .then(response => {
        if (response.ok) {
          this.fetchRequirements(); // Refrescar la lista después de actualizar
          requirement.editing = false; // Desactivar modo edición
        } else {
          console.error('Failed to update requirement');
        }
      })
      .catch(error => {
        console.error('Error updating requirement:', error);
      });
    },
    startEditing(requirement) {
      requirement.editing = true; // Activar modo edición
    },
    deleteRequirement(requirementId) {
      fetch(`${apiUrl}/test/${requirementId}`, {
        method: 'DELETE'
      })
      .then(response => {
        if (response.ok) {
          this.fetchRequirements(); // Refrescar la lista después de eliminar
        } else {
          console.error('Failed to delete requirement');
        }
      })
      .catch(error => {
        console.error('Error deleting requirement:', error);
      });
    },
    clearForm() {
      this.selectedAttribute = null;
      this.newRequirementText = '';
    }
  }
};
</script>

<style scoped>
.container {
  margin: 20px;
  align-items: left;
}

.add-button {
  margin-top: 20px;
  border: 2px solid rgb(44, 182, 125);
  background-color: transparent;
  color: rgb(44, 182, 125);
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  margin-bottom: 20px;
  width: 300px;
}

.add-button:hover {
  background-color: rgb(44, 182, 125);
  color: white;
}

.requirements-list {
  list-style-type: none;
  padding: 0;
}

.requirements-list li {
  display: flex; /* Utiliza flexbox para alinear horizontalmente los elementos */
  align-items: center; /* Centra verticalmente los elementos */
  justify-content: space-between; /* Distribuye los elementos horizontalmente */
  margin-bottom: 10px;
}

.requirements-list strong {
  margin-right: 10px;
}

.delete-button {
  color: red;
  cursor: pointer;
  margin-left: auto; /* Empuja el botón de eliminar hacia la derecha */
}

.delete-button:hover {
  color: darkred;
}


.editable-text {
  cursor: pointer;
}

.edit-input {
  width: calc(100% - 25px); /* Ajuste para el tamaño del span y el espacio para la "X" */
}

.save-indicator {
  color: green;
  margin-left: 5px;
}

/* Estilos para los botones Save y Cancel */
.add-requirement button {
  margin-top: 20px;
  border: 2px solid rgb(44, 182, 125);
  background-color: transparent;
  color: rgb(44, 182, 125);
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  margin-bottom: 20px;
  width: 100px;
}

.add-requirement button:hover {
  background-color: rgb(44, 182, 125);
  color: white; /* Color verde más oscuro al hacer hover */
}
</style>
