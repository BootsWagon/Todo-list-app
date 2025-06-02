<template>
  <div class="app">
    <el-container>
      <el-header>
        <h1>Todo List</h1>
      </el-header>
      <el-main>
        <task-list />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import TaskList from './components/TaskList.vue'

export default {
  name: 'App',
  components: {
    TaskList
  }
}
</script>

<style>
.app {
  font-family: Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin: 0;
  padding: 0;
}

.el-header {
  background-color: #409EFF;
  color: white;
  text-align: center;
  line-height: 60px;
}

.el-main {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
</style> 