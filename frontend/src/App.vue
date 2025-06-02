<template>
  <div class="app">
    <task-board />
  </div>
</template>

<script>
import TaskBoard from './components/TaskBoard.vue'

export default {
  name: 'App',
  components: {
    TaskBoard
  }
}
</script>

<style>
.app {
  margin: 0;
  padding: 0;
  font-family: 'Arial', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  margin: 0;
  padding: 0;
}
</style> 