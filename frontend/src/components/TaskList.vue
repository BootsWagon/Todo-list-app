<template>
  <div class="task-list">
    <el-card class="add-task">
      <el-form :model="newTask" @submit.prevent="addTask">
        <el-form-item>
          <el-input
            v-model="newTask.title"
            placeholder="Enter task title"
            required
          />
        </el-form-item>
        <el-form-item>
          <el-input
            v-model="newTask.description"
            type="textarea"
            placeholder="Enter task description"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit">Add Task</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card v-loading="loading" class="tasks">
      <template v-if="tasks.length">
        <div v-for="task in tasks" :key="task.id" class="task-item">
          <el-checkbox
            v-model="task.completed"
            @change="updateTask(task)"
          />
          <div class="task-content" :class="{ completed: task.completed }">
            <h3>{{ task.title }}</h3>
            <p>{{ task.description }}</p>
            <small>Created: {{ formatDate(task.created_at) }}</small>
          </div>
          <el-button
            type="danger"
            :icon="Delete"
            circle
            @click="deleteTask(task.id)"
          />
        </div>
      </template>
      <el-empty v-else description="No tasks yet" />
    </el-card>
  </div>
</template>

<script>
import { ref } from 'vue'
import { Delete } from '@element-plus/icons-vue'
import { TaskService } from '../services/api'
import { ElMessage } from 'element-plus'

export default {
  name: 'TaskList',
  setup() {
    const tasks = ref([])
    const loading = ref(false)
    const newTask = ref({
      title: '',
      description: ''
    })

    const fetchTasks = async () => {
      loading.value = true
      try {
        const response = await TaskService.getTasks()
        tasks.value = response.data.results || response.data
      } catch (error) {
        ElMessage.error('Error fetching tasks')
        console.error('Error:', error)
      } finally {
        loading.value = false
      }
    }

    const addTask = async () => {
      if (!newTask.value.title) return
      
      loading.value = true
      try {
        await TaskService.createTask(newTask.value)
        await fetchTasks()
        newTask.value = { title: '', description: '' }
        ElMessage.success('Task added successfully')
      } catch (error) {
        ElMessage.error('Error adding task')
        console.error('Error:', error)
      } finally {
        loading.value = false
      }
    }

    const updateTask = async (task) => {
      loading.value = true
      try {
        await TaskService.updateTask(task.id, task)
        ElMessage.success('Task updated successfully')
      } catch (error) {
        ElMessage.error('Error updating task')
        console.error('Error:', error)
      } finally {
        loading.value = false
      }
    }

    const deleteTask = async (id) => {
      loading.value = true
      try {
        await TaskService.deleteTask(id)
        await fetchTasks()
        ElMessage.success('Task deleted successfully')
      } catch (error) {
        ElMessage.error('Error deleting task')
        console.error('Error:', error)
      } finally {
        loading.value = false
      }
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleString()
    }

    // Fetch tasks when component is mounted
    fetchTasks()

    return {
      tasks,
      loading,
      newTask,
      addTask,
      updateTask,
      deleteTask,
      formatDate,
      Delete
    }
  }
}
</script>

<style scoped>
.task-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.add-task {
  margin-bottom: 20px;
}

.task-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.task-item:last-child {
  border-bottom: none;
}

.task-content {
  flex: 1;
}

.task-content.completed {
  text-decoration: line-through;
  color: #999;
}

.task-content h3 {
  margin: 0 0 5px 0;
}

.task-content p {
  margin: 0 0 5px 0;
  color: #666;
}

.task-content small {
  color: #999;
}
</style> 