<template>
  <div>
    <button @click="addRequirement" class="add-button">Add</button>
    <div class="container">
      <ul class="requirements-list">
        <li v-for="(requirement, index) in requirements" :key="requirement.id" class="requirement-item">
          <span 
            v-if="!requirement.editing"
            @click="startEditing(requirement, index)"
            class="editable-text"
          >{{ requirement.text }}</span>
          <input 
            v-else 
            type="text" 
            v-model="requirement.text" 
            @blur="saveRequirement(requirement)" 
            class="edit-input"
            :ref="'editInput' + index"
          >
          <span class="delete-button" @click="deleteRequirement(requirement.id)">❌</span>
        </li>
      </ul>
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
      newRequirementText: ''
    };
  },
  mounted() {
    this.fetchRequirements();
  },
  methods: {
    fetchRequirements() {
      fetch(`${apiUrl}/modeling/${this.selectedProblem}`)
        .then(response => response.json())
        .then(data => {
          this.requirements = data.map(req => ({ ...req, editing: false }));
        })
        .catch(error => {
          console.error('Error fetching requirements:', error);
        });
    },
    addRequirement() {
      const newRequirement = {
        text: "",
        problem_id: this.selectedProblem,
        editing: true // New requirement starts in editing mode
      };
      this.requirements.push(newRequirement);
      this.$nextTick(() => {
        const inputs = this.$refs;
        const lastInputKey = `editInput${this.requirements.length - 1}`;
        if (inputs[lastInputKey]) {
          inputs[lastInputKey][0].focus();
        }
      });
    },
    saveRequirement(requirement) {
      if (!requirement.id) {
        // If the requirement does not have an id, create a new one
        fetch(`${apiUrl}/modeling`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            text: requirement.text,
            problem_id: this.selectedProblem
          })
        })
        .then(response => response.json())
        .then(() => {
          this.fetchRequirements(); // Refresh the list after adding
        })
        .catch(error => {
          console.error('Error adding requirement:', error);
        });
      } else {
        // Update existing requirement
        fetch(`${apiUrl}/modeling/${requirement.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            text: requirement.text
          })
        })
        .then(response => response.json())
        .then(() => {
          requirement.editing = false; // Exit editing mode
        })
        .catch(error => {
          console.error('Error updating requirement:', error);
        });
      }
    },
    startEditing(requirement, index) {
      requirement.editing = true; // Activar modo edición
      this.$nextTick(() => {
        const input = this.$refs[`editInput${index}`];
        if (input && input[0]) {
          input[0].focus();
        }
      });
    },
    deleteRequirement(requirementId) {
      fetch(`${apiUrl}/modeling/${requirementId}`, {
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

.requirements-list .requirement-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  width: 100%;
  justify-content: space-between; /* Ensure items take full width */
}

.editable-text {
  flex-grow: 1;
  font-weight: bold;
  cursor: pointer;
  white-space: pre-wrap; /* Permite saltos de línea */
  text-align: left; /* Align text to the left */
}

.edit-input {
  flex-grow: 1;
  margin-right: 10px;
  font-weight: normal;
  width: 100%;
  text-align: left; /* Align text to the left */
}

.delete-button {
  color: red;
  cursor: pointer;
  margin-left: 10px;
}

.delete-button:hover {
  color: darkred;
}
</style>
