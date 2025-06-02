<template>
  <div class="task-board" :style="boardStyle">
    <el-row :gutter="20">
      <el-col :span="6" v-for="status in statuses" :key="status.value">
        <div class="board-column" :style="getColumnStyle(status.value)" :data-status="status.value">
          <h2 class="column-title" :style="getColumnTitleStyle(status.value)">
            <i :class="status.icon"></i>
            {{ status.label }}
          </h2>
          <draggable
            v-model="tasksByStatus[status.value]"
            :group="{ name: 'tasks', pull: true, put: true }"
            @change="(e) => handleDragChange(e, status.value)"
            @start="dragStart"
            @end="dragEnd"
            item-key="id"
            class="task-list"
            :disabled="loading"
            ghost-class="ghost-card"
            drag-class="dragging-card"
            animation="300"
          >
            <template #item="{ element: task }">
              <el-card 
                :class="['task-card', `priority-${task.priority.toLowerCase()}`]"
                :shadow="'hover'"
                :style="getCardStyle(task.status)"
                v-loading="loadingTasks[task.id]"
                element-loading-background="rgba(255, 255, 255, 0.7)"
                :data-task-id="task.id"
                :data-current-status="task.status"
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
                      :disabled="loading || loadingTasks[task.id]"
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
                          :disabled="loading || loadingTasks[task.id]"
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
        <el-button @click="dialogVisible = false" :disabled="loading">Cancel</el-button>
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
      :disabled="loading"
    >
      <el-icon><Plus /></el-icon>
    </el-button>

    <!-- Theme Customizer -->
    <theme-customizer :statuses="statuses" />
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import draggable from 'vuedraggable'
import { Delete, Plus, Edit } from '@element-plus/icons-vue'
import { TaskService } from '../services/api'
import { useThemeStore } from '../stores/themeStore'
import ThemeCustomizer from './ThemeCustomizer.vue'

export default {
  name: 'TaskBoard',
  components: {
    draggable,
    Plus,
    ThemeCustomizer
  },
  setup() {
    const tasks = ref([])
    const loading = ref(false)
    const loadingTasks = ref({})
    const dialogVisible = ref(false)
    const editingTask = ref(null)
    const taskFormRef = ref(null)
    const taskForm = ref({
      title: '',
      description: '',
      status: 'UPCOMING',
      priority: 'MEDIUM'
    })

    // Create a local copy of tasks grouped by status to prevent flickering
    const localTasksByStatus = ref({})

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

    // Watch for changes in tasksByStatus and update localTasksByStatus
    watch(tasksByStatus, (newValue) => {
      Object.keys(newValue).forEach(status => {
        localTasksByStatus.value[status] = newValue[status]
      })
    }, { immediate: true, deep: true })

    const { currentTheme } = useThemeStore()

    // Watch for changes in currentTheme and force a re-render of the board
    watch(() => currentTheme.value, () => {
      // Force re-render by creating a new array reference
      tasks.value = [...tasks.value]
    }, { deep: true })

    const setTaskLoading = (taskId, isLoading) => {
      loadingTasks.value = {
        ...loadingTasks.value,
        [taskId]: isLoading
      }
    }

    const boardStyle = computed(() => ({
      background: currentTheme.value.boardBackground,
      ...(currentTheme.value.boardBackgroundImage && {
        backgroundImage: `url(${currentTheme.value.boardBackgroundImage})`,
        backgroundSize: currentTheme.value.boardImageFit || 'cover',
        backgroundPosition: currentTheme.value.boardImagePosition || 'center center',
        backgroundRepeat: 'no-repeat'
      })
    }))

    const getColumnStyle = (status) => {
      const opacity = currentTheme.value.columnOpacity?.[status] || 0.1;
      const baseStyle = {
        '--column-opacity': opacity,
        backgroundColor: currentTheme.value.columnBackgrounds[status] || `rgba(255, 255, 255, ${opacity})`
      };

      if (currentTheme.value.columnBackgroundImages?.[status]) {
        return {
          ...baseStyle,
          '--column-bg-image': `url(${currentTheme.value.columnBackgroundImages[status]})`,
          '--column-bg-size': currentTheme.value.columnImageFit?.[status] || 'cover',
          '--column-bg-position': currentTheme.value.columnImagePosition?.[status] || 'center center'
        };
      }

      return baseStyle;
    }

    const getColumnTitleStyle = (status) => ({
      color: currentTheme.value.columnTitleColors[status]
    })

    const getCardStyle = (status) => {
      const opacity = currentTheme.value.cardOpacity?.[status] || 0.95;
      const baseStyle = {
        '--card-opacity': opacity,
        backgroundColor: currentTheme.value.cardBackgrounds[status] || `rgba(255, 255, 255, ${opacity})`
      };

      if (currentTheme.value.cardBackgroundImages?.[status]) {
        return {
          ...baseStyle,
          '--card-bg-image': `url(${currentTheme.value.cardBackgroundImages[status]})`,
          '--card-bg-size': currentTheme.value.cardImageFit?.[status] || 'cover',
          '--card-bg-position': currentTheme.value.cardImagePosition?.[status] || 'center center'
        };
      }

      return baseStyle;
    }

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
        console.log('Fetched tasks:', tasks.value)
        console.log('Tasks by status:', tasksByStatus.value)
      } catch (error) {
        ElMessage.error('Error fetching tasks')
        console.error('Error:', error)
      } finally {
        loading.value = false
      }
    }

    const updateTaskInStore = (updatedTask) => {
      // First update the main tasks array
      const taskIndex = tasks.value.findIndex(t => t.id === updatedTask.id);
      if (taskIndex !== -1) {
        tasks.value[taskIndex] = { ...updatedTask };
        
        // Then explicitly update the task in the correct status column
        Object.keys(localTasksByStatus.value).forEach(status => {
          const statusTasks = localTasksByStatus.value[status];
          const statusTaskIndex = statusTasks.findIndex(t => t.id === updatedTask.id);
          
          if (status === updatedTask.status) {
            // Add to new status if not present
            if (statusTaskIndex === -1) {
              localTasksByStatus.value[status].push({ ...updatedTask });
            } else {
              // Update in current status
              localTasksByStatus.value[status][statusTaskIndex] = { ...updatedTask };
            }
          } else if (statusTaskIndex !== -1) {
            // Remove from old status
            localTasksByStatus.value[status].splice(statusTaskIndex, 1);
          }
        });
      }
      
      // Force a re-render of the columns
      localTasksByStatus.value = { ...localTasksByStatus.value };
    };

    const currentDrag = ref(null);

    const dragStart = (evt) => {
      const taskId = evt.item.getAttribute('data-task-id');
      const currentStatus = evt.item.getAttribute('data-current-status');
      console.log('Drag started:', { taskId, currentStatus });
      currentDrag.value = {
        taskId,
        originalStatus: currentStatus
      };
    };

    const dragEnd = (evt) => {
      console.log('Drag ended:', evt);
      currentDrag.value = null;
    };

    const handleDragChange = async (event, targetStatus) => {
      console.log('Drag change event:', { event, targetStatus });
      
      if (!event) {
        console.log('No event data received');
        return;
      }

      const { added, moved, removed } = event;
      
      if (added) {
        const task = added.element;
        if (!task?.id) {
          console.log('No task id found');
          return;
        }

        console.log('Task added to column:', {
          taskId: task.id,
          currentStatus: task.status,
          targetStatus: targetStatus,
          originalStatus: currentDrag.value?.originalStatus
        });

        // Create a complete update object with the new status
        const updatedTask = {
          ...task,
          originalStatus: task.status,
          status: targetStatus, // Use the target column's status
          order: added.newIndex
        };

        console.log('Updating task with:', updatedTask);

        const success = await handleTaskUpdate(task.id, updatedTask);
        
        if (!success) {
          console.log('Task update failed, reverting...');
          await fetchTasks();
        }
      } else if (moved) {
        const task = moved.element;
        if (!task?.id) return;

        console.log('Task moved within same column:', {
          taskId: task.id,
          status: targetStatus,
          newIndex: moved.newIndex
        });

        // For moves within the same column, only update order
        const updatedTask = {
          ...task,
          order: moved.newIndex
        };

        await handleTaskUpdate(task.id, updatedTask);
      }

      if (removed) {
        console.log('Task removed from column:', {
          element: removed.element,
          oldIndex: removed.oldIndex
        });
      }
    };

    const handleTaskUpdate = async (taskId, updates) => {
      console.log('Sending task update to server:', { taskId, updates });
      setTaskLoading(taskId, true);
      
      try {
        const response = await TaskService.updateTask(taskId, updates);
        
        if (response.data) {
          console.log('Server response:', response.data);
          updateTaskInStore(response.data);
          return true;
        } else {
          throw new Error('No data received from server');
        }
      } catch (error) {
        console.error('Error updating task:', error);
        const errorMessage = error?.response?.data?.message || 'Failed to update task';
        ElMessage.error(errorMessage);
        await fetchTasks(); // Revert UI changes
        return false;
      } finally {
        setTaskLoading(taskId, false);
      }
    };

    // Improve the watch to handle status updates more reliably
    watch(tasks, (newTasks) => {
      // First, ensure all status arrays exist and are empty
      statuses.forEach(status => {
        localTasksByStatus.value[status.value] = [];
      });

      // Then populate with current tasks
      newTasks.forEach(task => {
        const status = task.status;
        if (status && localTasksByStatus.value[status]) {
          localTasksByStatus.value[status].push(task);
        } else {
          console.error(`Invalid status ${status} for task:`, task);
        }
      });

      // Sort tasks by order within each status
      Object.keys(localTasksByStatus.value).forEach(status => {
        localTasksByStatus.value[status].sort((a, b) => a.order - b.order);
      });
    }, { deep: true, immediate: true });

    // Add debugging to track task status changes
    watch(localTasksByStatus, (newValue, oldValue) => {
      if (!oldValue) return;
      
      Object.keys(newValue).forEach(status => {
        const newTasks = newValue[status];
        const oldTasks = oldValue[status] || [];
        
        // Check for tasks that moved into this status
        const addedTasks = newTasks.filter(task => 
          !oldTasks.some(oldTask => oldTask.id === task.id)
        );
        
        // Check for tasks that moved out of this status
        const removedTasks = oldTasks.filter(task => 
          !newTasks.some(newTask => newTask.id === task.id)
        );
        
        if (addedTasks.length > 0 || removedTasks.length > 0) {
          console.log(`Status ${status} changes:`, {
            added: addedTasks.map(t => ({ id: t.id, status: t.status })),
            removed: removedTasks.map(t => ({ id: t.id, status: t.status }))
          });
        }
      });
    }, { deep: true });

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
              const response = await TaskService.updateTask(editingTask.value.id, taskForm.value)
              const updatedTask = response.data
              const index = tasks.value.findIndex(t => t.id === updatedTask.id)
              if (index !== -1) {
                tasks.value[index] = updatedTask
              }
              ElMessage.success('Task updated successfully')
            } else {
              const response = await TaskService.createTask(taskForm.value)
              tasks.value = [...tasks.value, response.data]
              ElMessage.success('Task created successfully')
            }
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

    const deleteTask = async (id) => {
      setTaskLoading(id, true)
      try {
        await TaskService.deleteTask(id)
        tasks.value = tasks.value.filter(task => task.id !== id)
        ElMessage.success('Task deleted successfully')
      } catch (error) {
        ElMessage.error('Error deleting task')
        console.error('Error:', error)
      } finally {
        setTaskLoading(id, false)
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
      loadingTasks,
      dialogVisible,
      editingTask,
      taskForm,
      taskFormRef,
      rules,
      statuses,
      priorities,
      tasksByStatus: localTasksByStatus, // Use the local copy for the template
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
      Edit,
      boardStyle,
      getColumnStyle,
      getColumnTitleStyle,
      getCardStyle,
      dragStart,
      dragEnd
    }
  }
}
</script>

<style scoped>
.task-board {
  min-height: 100vh;
  padding: 2rem;
  color: #fff;
  position: relative;
  background-color: #1a1a2e; /* Fallback color */
}

.board-column {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 1rem;
  height: calc(100vh - 100px);
  overflow-y: auto;
  backdrop-filter: blur(5px);
  position: relative;
  transition: all 0.3s ease;
}

.board-column::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: inherit;
  background-image: var(--column-bg-image);
  background-size: var(--column-bg-size, cover);
  background-position: var(--column-bg-position, center center);
  background-repeat: no-repeat;
  opacity: var(--column-opacity, 0.1);
  z-index: 0;
  pointer-events: none;
  border-radius: inherit;
}

.board-column::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, var(--column-opacity, 0.1));
  z-index: 0;
  pointer-events: none;
  border-radius: inherit;
}

.board-column > * {
  position: relative;
  z-index: 1;
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
  padding: 8px;
  height: calc(100% - 50px); /* Subtract header height */
  overflow-y: auto;
}

.ghost-card {
  opacity: 0.5;
  background: #c8ebfb !important;
  border: 2px dashed #409eff !important;
  cursor: move;
}

.ghost-card * {
  opacity: 0;
}

.dragging-card {
  transform: rotate(2deg) scale(1.02);
  cursor: grabbing;
}

.task-card {
  margin-bottom: 1rem;
  border-radius: 8px;
  transition: all 0.2s ease;
  backdrop-filter: blur(5px);
  cursor: grab;
  position: relative;
  overflow: hidden;
  transform-origin: center center;
  background-color: var(--card-bg-color, rgba(255, 255, 255, 0.95));
}

.task-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: inherit;
  background-image: var(--card-bg-image);
  background-size: var(--card-bg-size, cover);
  background-position: var(--card-bg-position, center center);
  background-repeat: no-repeat;
  opacity: var(--card-opacity, 0.95);
  z-index: 0;
  pointer-events: none;
}

.task-card::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, var(--card-opacity, 0.95));
  z-index: 0;
  pointer-events: none;
}

.task-card > * {
  position: relative;
  z-index: 1;
}

.task-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.task-card:active {
  cursor: grabbing;
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

.task-card .task-header,
.task-card .task-description,
.task-card .task-footer {
  position: relative;
  z-index: 1;
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