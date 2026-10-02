<template>
  <div class="container">
    <button v-if="!selectedProblem" class="load-button" @click="createNewProblem">New Problem</button>
    
    <div class="problem-selector">
      <select v-model="selectedProblem" @change="fetchProblemData" class="lab-select">
        <option :value="null" disabled>Select an existing problem</option>
        <option v-for="problem in problems" :value="problem.id" :key="problem.id">Problem-{{ problem.id }}</option>
      </select>
      <button v-if="selectedProblem" class="delete-button" @click="confirmDelete(selectedProblem)">Delete Problem</button>
    </div>
    
    
  </div>
</template>


<script>
const apiUrl = process.env.VUE_APP_API_URL;
import axios from 'axios';

export default {
  props: ['selectedLab'],
  data() {
    return {
      selectedProblem: null,
      problems: [],
      problemInfo: null,
      livingLab: null
    };
  },
  created() {
    this.fetchProblems();
  },
  methods: {
    async fetchProblems() {
      try {
        const response = await axios.get(`${apiUrl}/problem`);
        this.problems = response.data;
        console.log('Problems:', this.problems);
      } catch (error) {
        console.error('Error fetching problems:', error);
      }
    },
    async fetchProblemData() {
      if (this.selectedProblem) {
        try {
          this.problemInfo = null;
          const response = await axios.post(`${apiUrl}/problem_data`, { problemId: this.selectedProblem });
          this.problemInfo = response.data;
          this.livingLab = this.problemInfo.context_id;
          this.$emit('selectedProblem', this.selectedProblem);
          this.$emit('selectedLivingLab', this.livingLab);
           // faire plutot un emit de problemInfo (comme ça il y a le need, le context, ...)
          console.log('Problem data:', this.selectedProblem);
          console.log('LivingLab data:', this.livingLab);
        } catch (error) {
          console.error('Error fetching problem data:', error);
        }
      }
    },
    async createNewProblem() {
      try {
        const response = await axios.post(`${apiUrl}/problem`);
        const newProblemId = response.data.problemId;
        this.selectedProblem = newProblemId;
        await this.fetchProblems(); // Refresh the list of problems
        this.fetchProblemData(); // Fetch data for the new problem
      } catch (error) {
        console.error('Error creating new problem:', error);
      }
    },
    confirmDelete(problemId) {
      if (confirm('Are you sure you want to delete this problem?')) {
        this.deleteProblem(problemId);
      }
    },
    async deleteProblem(problemId) {
      try {
        await axios.delete(`${apiUrl}/problem/${problemId}`);
        await this.fetchProblems(); // Refresh the list of problems after deletion
        if (this.selectedProblem === problemId) {
          this.selectedProblem = null; // Reset selected problem if it was deleted
          this.problemInfo = null; // Clear problem info if the selected problem was deleted
        }
      } catch (error) {
        console.error('Error deleting problem:', error);
      }
    }
  }
  ,  watch: {
    selectedLab(newVal, oldVal) {
      if (newVal !== oldVal) {
        console.log('selectedLab has changed:', newVal);
        this.fetchProblemData();
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
  height: 20vh;
  margin-right: 15%;
}

.problem-selector {
  display: flex;
  align-items: center;
  
  width: 23%;
}

.load-button,
.delete-button {
  padding: 10px 20px;
  border: 2px solid rgb(44, 182, 125);
  background-color: transparent;
  color: rgb(44, 182, 125);
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  margin-bottom: 20px;
  margin-left: 10px;
  
  
  width: 25%;
}

.load-button:hover,
.delete-button:hover {
  background-color: rgb(44, 182, 125);
  color: white;
}

.problem-selector .delete-button {
  border-color: red;
  color: red;
  align-self: flex-end;
  width: 50%;
  margin-left: 190%;
  
  font-size: small;
  
   
}

.delete-button:hover {
  background-color: red;
  color: white;
}

.text-box {
  align-self: flex-start;
  color: rgb(58, 59, 57);
  font-size: 36px;
  font-family: sans-serif;
  font-weight: 200;
  padding-left: 20px;
}

.lab-select {
  width: auto;
  padding: 10px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #ccc;
  margin-bottom: 20px;
}

</style>
