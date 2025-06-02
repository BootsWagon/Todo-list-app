<template>
  <div class="task-board space-theme">
    <el-row :gutter="20">
      <el-col :span="6" v-for="status in statuses" :key="status.value">
        <div class="board-column">
          <h2 class="column-title">
            <i :class="status.icon"></i>
            {{ status.label }}
          </h2>
          <draggable
            v-model="tasksByStatus[status.value]"
            group="tasks"
            @change="handleDragChange"
            item-key="id"
            class="task-list"
          >
            <template #item="{ element: task }">
              <el-card 
                :class="['task-card', `priority-${task.priority.toLowerCase()}`]"
                :shadow="'hover'"
              >
                <div class="task-header">
                  <el-tag :type="getPriorityType(task.priority)">
                    {{ task.priority_display }}
                  </el-tag>
                  <div class="task-actions">
                    <el-button
                      type="primary"
                      :icon="Edit"
                      circle
                      size="small"
                      @click="editTask(task)"
                    />
                    <el-popconfirm
                      title="Are you sure you want to delete this task?"
                      @confirm="deleteTask(task.id)"
                    >
                      <template #reference>
                        <el-button
                          type="danger"
                          :icon="Delete"
                          circle
                          size="small"
                        />
                      </template>
                    </el-popconfirm>
                  </div>
                </div>
                <h3>{{ task.title }}</h3>
                <p class="task-description">{{ task.description }}</p>
                <div class="task-footer">
                  <small>Created: {{ formatDate(task.created_at) }}</small>
                  <small v-if="task.updated_at !== task.created_at">
                    · Updated: {{ formatDate(task.updated_at) }}
                  </small>
                </div>
              </el-card>
            </template>
          </draggable>
        </div>
      </el-col>
    </el-row>

    <!-- Task Dialog (Add/Edit) -->
    <el-dialog
      v-model="dialogVisible"
      :title="editingTask ? 'Edit Task' : 'Add New Task'"
      width="500px"
      :close-on-click-modal="false"
      @closed="resetForm"
    >
      <el-form 
        :model="taskForm" 
        label-width="120px"
        :rules="rules"
        ref="taskFormRef"
      >
        <el-form-item label="Title" prop="title">
          <el-input 
            v-model="taskForm.title"
            placeholder="Enter task title"
            :maxlength="200"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="Description" prop="description">
          <el-input
            v-model="taskForm.description"
            type="textarea"
            :rows="3"
            placeholder="Enter task description"
            :maxlength="1000"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="Status" prop="status">
          <el-select v-model="taskForm.status" style="width: 100%">
            <el-option
              v-for="status in statuses"
              :key="status.value"
              :label="status.label"
              :value="status.value"
            >
              <span style="float: left">
                <i :class="status.icon" style="margin-right: 8px"></i>
                {{ status.label }}
              </span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Priority" prop="priority">
          <el-select v-model="taskForm.priority" style="width: 100%">
            <el-option
              v-for="priority in priorities"
              :key="priority.value"
              :label="priority.label"
              :value="priority.value"
            >
              <el-tag :type="getPriorityType(priority.value)" size="small">
                {{ priority.label }}
              </el-tag>
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="saveTask" :loading="loading">
          {{ editingTask ? 'Update' : 'Create' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- Add Task Button -->
    <el-button
      class="add-task-btn"
      type="primary"
      size="large"
      circle
      @click="showAddTaskDialog"
    >
      <el-icon><Plus /></el-icon>
    </el-button>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import draggable from 'vuedraggable'
import { Delete, Plus, Edit } from '@element-plus/icons-vue'
import { TaskService } from '../services/api'

export default {
  name: 'TaskBoard',
  components: {
    draggable,
    Plus
  },
  setup() {
    const tasks = ref([])
    const loading = ref(false)
    const dialogVisible = ref(false)
    const editingTask = ref(null)
    const taskFormRef = ref(null)
    const taskForm = ref({
      title: '',
      description: '',
      status: 'UPCOMING',
      priority: 'MEDIUM'
    })

    const rules = {
      title: [
        { required: true, message: 'Please enter a title', trigger: 'blur' },
        { min: 3, message: 'Title must be at least 3 characters', trigger: 'blur' }
      ],
      status: [
        { required: true, message: 'Please select a status', trigger: 'change' }
      ],
      priority: [
        { required: true, message: 'Please select a priority', trigger: 'change' }
      ]
    }

    const statuses = [
      { value: 'ON_HOLD', label: 'On Hold', icon: 'el-icon-time' },
      { value: 'CURRENT', label: 'Current', icon: 'el-icon-loading' },
      { value: 'UPCOMING', label: 'Upcoming', icon: 'el-icon-star-off' },
      { value: 'COMPLETED', label: 'Completed', icon: 'el-icon-check' }
    ]

    const priorities = [
      { value: 'LOW', label: 'Low' },
      { value: 'MEDIUM', label: 'Medium' },
      { value: 'HIGH', label: 'High' }
    ]

    const tasksByStatus = computed(() => {
      const grouped = {}
      statuses.forEach(status => {
        grouped[status.value] = tasks.value.filter(task => task.status === status.value)
      })
      return grouped
    })

    const resetForm = () => {
      if (taskFormRef.value) {
        taskFormRef.value.resetFields()
      }
      editingTask.value = null
      taskForm.value = {
        title: '',
        description: '',
        status: 'UPCOMING',
        priority: 'MEDIUM'
      }
    }

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

    const handleDragChange = async ({ added, moved }) => {
      if (added) {
        const { element: task, newIndex } = added
        const newStatus = Object.entries(tasksByStatus.value).find(([,tasks]) => 
          tasks.includes(task)
        )?.[0] || task.status
        task.status = newStatus
        task.order = newIndex
        await updateTask(task)
      } else if (moved) {
        const { element: task, newIndex } = moved
        task.order = newIndex
        await updateTask(task)
      }
    }

    const showAddTaskDialog = () => {
      resetForm()
      dialogVisible.value = true
    }

    const editTask = (task) => {
      editingTask.value = task
      taskForm.value = { ...task }
      dialogVisible.value = true
    }

    const saveTask = async () => {
      if (!taskFormRef.value) return

      await taskFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            if (editingTask.value) {
              await TaskService.updateTask(editingTask.value.id, taskForm.value)
              ElMessage.success('Task updated successfully')
            } else {
              await TaskService.createTask(taskForm.value)
              ElMessage.success('Task created successfully')
            }
            await fetchTasks()
            dialogVisible.value = false
          } catch (error) {
            ElMessage.error(editingTask.value ? 'Error updating task' : 'Error creating task')
            console.error('Error:', error)
          } finally {
            loading.value = false
          }
        }
      })
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

    const getPriorityType = (priority) => {
      const types = {
        LOW: 'info',
        MEDIUM: 'warning',
        HIGH: 'danger'
      }
      return types[priority] || 'info'
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleString()
    }

    onMounted(() => {
      fetchTasks()
    })

    return {
      tasks,
      loading,
      dialogVisible,
      editingTask,
      taskForm,
      taskFormRef,
      rules,
      statuses,
      priorities,
      tasksByStatus,
      handleDragChange,
      showAddTaskDialog,
      editTask,
      saveTask,
      deleteTask,
      getPriorityType,
      formatDate,
      resetForm,
      Delete,
      Plus,
      Edit
    }
  }
}
</script>

<style scoped>
.space-theme {
  background: linear-gradient(to bottom, #1a1a2e, #16213e);
  min-height: 100vh;
  padding: 2rem;
  color: #fff;
}

.board-column {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 1rem;
  height: calc(100vh - 100px);
  overflow-y: auto;
}

.column-title {
  color: #fff;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.task-list {
  min-height: 200px;
}

.task-card {
  margin-bottom: 1rem;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.95);
  transition: all 0.3s ease;
}

.task-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.task-actions {
  display: flex;
  gap: 8px;
}

.task-description {
  color: #666;
  margin: 8px 0;
  white-space: pre-line;
}

.task-footer {
  margin-top: 0.5rem;
  color: #666;
  font-size: 0.85em;
  display: flex;
  gap: 8px;
}

.priority-high {
  border-left: 4px solid #f56c6c;
}

.priority-medium {
  border-left: 4px solid #e6a23c;
}

.priority-low {
  border-left: 4px solid #409eff;
}

.add-task-btn {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 60px;
  height: 60px;
  font-size: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Scrollbar styling */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.4);
}
</style> 