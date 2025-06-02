<template>
  <div>
    <el-button type="primary" @click="showDialog" class="customize-theme-btn">
      <el-icon><Brush /></el-icon>
      Customize Theme
    </el-button>

    <el-dialog
      v-model="dialogVisible"
      title="Customize Theme"
      width="600px"
      :close-on-click-modal="false"
      :before-close="handleClose"
    >
      <el-tabs v-model="activeTab" v-loading="saving">
        <el-tab-pane label="Board">
          <el-form label-position="top">
            <el-form-item label="Board Background">
              <el-color-picker
                v-model="themeForm.boardBackground"
                show-alpha
              />
            </el-form-item>
            <el-form-item label="Background Image">
              <div class="image-upload">
                <el-upload
                  class="upload-demo"
                  action="#"
                  :auto-upload="false"
                  :show-file-list="false"
                  accept="image/*"
                  @change="handleBoardImageUpload"
                >
                  <el-button type="primary">Select Image</el-button>
                </el-upload>
                <el-button 
                  v-if="themeForm.boardBackgroundImage" 
                  type="danger" 
                  @click="clearBoardImage"
                >
                  Clear Image
                </el-button>
              </div>
              <div v-if="themeForm.boardBackgroundImage">
                <div class="image-fit-controls">
                  <el-radio-group v-model="themeForm.boardImageFit">
                    <el-radio-button label="cover">Cover</el-radio-button>
                    <el-radio-button label="contain">Contain</el-radio-button>
                  </el-radio-group>
                </div>
                <div class="image-position-controls">
                  <el-select v-model="themeForm.boardImagePosition">
                    <el-option label="Center" value="center center" />
                    <el-option label="Top" value="center top" />
                    <el-option label="Bottom" value="center bottom" />
                    <el-option label="Left" value="left center" />
                    <el-option label="Right" value="right center" />
                  </el-select>
                </div>
                <div class="preview-image">
                  <img :src="themeForm.boardBackgroundImage" alt="Board background" />
                </div>
              </div>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="Columns">
          <el-form label-position="top" v-loading="saving">
            <div v-for="status in statuses" :key="status.value" class="status-section">
              <h3>{{ status.label }}</h3>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="Column Background">
                    <el-color-picker
                      v-model="themeForm.columnBackgrounds[status.value]"
                      show-alpha
                    />
                    <div class="opacity-control">
                      <span>Column Opacity:</span>
                      <el-slider
                        v-model="themeForm.columnOpacity[status.value]"
                        :min="0"
                        :max="1"
                        :step="0.05"
                      />
                    </div>
                    <div class="image-upload">
                      <el-upload
                        class="upload-demo"
                        action="#"
                        :auto-upload="false"
                        :show-file-list="false"
                        accept="image/*"
                        @change="(file) => handleColumnImageUpload(status.value, file)"
                      >
                        <el-button type="primary">Select Image</el-button>
                      </el-upload>
                      <el-button 
                        v-if="themeForm.columnBackgroundImages[status.value]" 
                        type="danger" 
                        @click="() => clearColumnImage(status.value)"
                      >
                        Clear Image
                      </el-button>
                    </div>
                    <div v-if="themeForm.columnBackgroundImages[status.value]">
                      <div class="image-fit-controls">
                        <el-radio-group 
                          v-model="themeForm.columnImageFit[status.value]"
                        >
                          <el-radio-button label="cover">Cover</el-radio-button>
                          <el-radio-button label="contain">Contain</el-radio-button>
                        </el-radio-group>
                      </div>
                      <div class="image-position-controls">
                        <el-select 
                          v-model="themeForm.columnImagePosition[status.value]"
                        >
                          <el-option label="Center" value="center center" />
                          <el-option label="Top" value="center top" />
                          <el-option label="Bottom" value="center bottom" />
                          <el-option label="Left" value="left center" />
                          <el-option label="Right" value="right center" />
                        </el-select>
                      </div>
                    </div>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="Card Settings">
                    <el-color-picker
                      v-model="themeForm.cardBackgrounds[status.value]"
                      show-alpha
                    />
                    <div class="image-upload">
                      <el-upload
                        class="upload-demo"
                        action="#"
                        :auto-upload="false"
                        :show-file-list="false"
                        accept="image/*"
                        @change="(file) => handleCardImageUpload(status.value, file)"
                      >
                        <el-button type="primary">Select Image</el-button>
                      </el-upload>
                      <el-button 
                        v-if="themeForm.cardBackgroundImages[status.value]" 
                        type="danger" 
                        @click="() => clearCardImage(status.value)"
                      >
                        Clear Image
                      </el-button>
                    </div>
                    <div v-if="themeForm.cardBackgroundImages[status.value]">
                      <div class="image-fit-controls">
                        <el-radio-group 
                          v-model="themeForm.cardImageFit[status.value]"
                        >
                          <el-radio-button label="cover">Cover</el-radio-button>
                          <el-radio-button label="contain">Contain</el-radio-button>
                        </el-radio-group>
                      </div>
                      <div class="image-position-controls">
                        <el-select 
                          v-model="themeForm.cardImagePosition[status.value]"
                        >
                          <el-option label="Center" value="center center" />
                          <el-option label="Top" value="center top" />
                          <el-option label="Bottom" value="center bottom" />
                          <el-option label="Left" value="left center" />
                          <el-option label="Right" value="right center" />
                        </el-select>
                      </div>
                    </div>
                    <div class="opacity-control">
                      <span>Card Opacity:</span>
                      <el-slider
                        v-model="themeForm.cardOpacity[status.value]"
                        :min="0"
                        :max="1"
                        :step="0.05"
                      />
                    </div>
                  </el-form-item>
                </el-col>
              </el-row>
              <div v-if="themeForm.columnBackgroundImages[status.value] || themeForm.cardBackgroundImages[status.value]" class="preview-images">
                <div v-if="themeForm.columnBackgroundImages[status.value]" class="preview-image">
                  <small>Column Background</small>
                  <img :src="themeForm.columnBackgroundImages[status.value]" :alt="'Column background for ' + status.label" />
                </div>
                <div v-if="themeForm.cardBackgroundImages[status.value]" class="preview-image">
                  <small>Card Background</small>
                  <img :src="themeForm.cardBackgroundImages[status.value]" :alt="'Card background for ' + status.label" />
                </div>
              </div>
            </div>
          </el-form>
        </el-tab-pane>
      </el-tabs>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleClose" :disabled="saving">Cancel</el-button>
          <el-button type="warning" @click="handleReset" :disabled="saving">Reset to Default</el-button>
          <el-button type="primary" @click="handleSave" :loading="saving">
            Save Changes
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- Unsaved Changes Dialog -->
    <el-dialog
      v-model="showUnsavedDialog"
      title="Unsaved Changes"
      width="400px"
      :close-on-click-modal="false"
    >
      <span>You have unsaved changes. Do you want to save them before closing?</span>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="handleDiscardChanges" :disabled="saving">Don't Save</el-button>
          <el-button type="primary" @click="handleSaveAndClose" :loading="saving">
            Save & Close
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { Brush } from '@element-plus/icons-vue'
import { useThemeStore } from '../stores/themeStore'
import { ElMessage } from 'element-plus'

export default {
  name: 'ThemeCustomizer',
  components: {
    Brush
  },
  props: {
    statuses: {
      type: Array,
      required: true
    }
  },
  setup() {
    const dialogVisible = ref(false)
    const showUnsavedDialog = ref(false)
    const saving = ref(false)
    const activeTab = ref('Board')
    const { currentTheme, updateTheme, resetTheme } = useThemeStore()
    const uploadLoading = ref(false)
    
    // Keep track of original theme when dialog opens
    const originalTheme = ref(null)
    const themeForm = ref({})

    const hasUnsavedChanges = computed(() => {
      if (!originalTheme.value) return false;
      return JSON.stringify(themeForm.value) !== JSON.stringify(originalTheme.value);
    });

    const showDialog = () => {
      originalTheme.value = JSON.parse(JSON.stringify(currentTheme.value));
      themeForm.value = JSON.parse(JSON.stringify(currentTheme.value));
      dialogVisible.value = true;
    };

    const handleClose = () => {
      if (hasUnsavedChanges.value) {
        showUnsavedDialog.value = true;
      } else {
        dialogVisible.value = false;
      }
    };

    const handleImageUpload = async (file) => {
      return new Promise((resolve, reject) => {
        // Check file size (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
          ElMessage.error('Image size should not exceed 5MB')
          reject(new Error('File too large'))
          return
        }

        const reader = new FileReader()
        reader.onload = (e) => {
          // Create an image element to resize the image
          const img = new Image();
          img.onload = () => {
            // Create canvas for resizing
            const canvas = document.createElement('canvas');
            let width = img.width;
            let height = img.height;
            
            // Calculate new dimensions (max 800px width/height)
            const maxSize = 800;
            if (width > maxSize || height > maxSize) {
              if (width > height) {
                height = Math.round((height * maxSize) / width);
                width = maxSize;
              } else {
                width = Math.round((width * maxSize) / height);
                height = maxSize;
              }
            }

            canvas.width = width;
            canvas.height = height;
            
            // Draw resized image
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, width, height);
            
            // Get compressed image data
            const compressedImage = canvas.toDataURL('image/jpeg', 0.7);
            resolve(compressedImage);
          };
          img.onerror = () => reject(new Error('Failed to load image'));
          img.src = e.target.result;
        };
        reader.onerror = (e) => reject(e);
        reader.readAsDataURL(file);
      });
    };

    const handleSave = async () => {
      saving.value = true;
      try {
        await updateTheme(themeForm.value);
        ElMessage.success('Theme settings saved successfully');
        originalTheme.value = JSON.parse(JSON.stringify(themeForm.value));
        dialogVisible.value = false;
      } catch (error) {
        if (error.response?.status === 413) {
          ElMessage.error('Theme data is too large. Try using fewer or smaller images.');
        } else {
          ElMessage.error('Failed to save theme settings');
        }
        console.error('Error saving theme:', error);
      } finally {
        saving.value = false;
      }
    };

    const handleSaveAndClose = async () => {
      saving.value = true;
      try {
        await updateTheme(themeForm.value);
        ElMessage.success('Theme settings saved successfully');
        originalTheme.value = JSON.parse(JSON.stringify(themeForm.value));
        showUnsavedDialog.value = false;
        dialogVisible.value = false;
      } catch (error) {
        if (error.response?.status === 413) {
          ElMessage.error('Theme data is too large. Try using fewer or smaller images.');
        } else {
          ElMessage.error('Failed to save theme settings');
        }
        console.error('Error saving theme:', error);
      } finally {
        saving.value = false;
      }
    };

    const handleDiscardChanges = () => {
      themeForm.value = JSON.parse(JSON.stringify(originalTheme.value));
      showUnsavedDialog.value = false;
      dialogVisible.value = false;
    };

    const handleReset = async () => {
      try {
        saving.value = true;
        await resetTheme();
        themeForm.value = JSON.parse(JSON.stringify(currentTheme.value));
        originalTheme.value = JSON.parse(JSON.stringify(currentTheme.value));
        ElMessage.success('Theme reset to default');
      } catch (error) {
        ElMessage.error('Failed to reset theme');
        console.error('Error resetting theme:', error);
      } finally {
        saving.value = false;
      }
    };

    const handleBoardImageUpload = async (file) => {
      uploadLoading.value = true
      try {
        const imageUrl = await handleImageUpload(file.raw)
        themeForm.value = { 
          ...themeForm.value, 
          boardBackgroundImage: imageUrl
        }
        ElMessage.success('Board background image updated')
      } catch (error) {
        if (!error.message?.includes('File too large')) {
          ElMessage.error('Error uploading image')
        }
      } finally {
        uploadLoading.value = false
      }
    }

    const handleColumnImageUpload = async (status, file) => {
      uploadLoading.value = true
      try {
        const imageUrl = await handleImageUpload(file.raw)
        themeForm.value = {
          ...themeForm.value,
          columnBackgroundImages: {
            ...themeForm.value.columnBackgroundImages,
            [status]: imageUrl
          }
        }
        ElMessage.success('Column background image updated')
      } catch (error) {
        if (!error.message?.includes('File too large')) {
          ElMessage.error('Error uploading image')
        }
      } finally {
        uploadLoading.value = false
      }
    }

    const handleCardImageUpload = async (status, file) => {
      uploadLoading.value = true
      try {
        const imageUrl = await handleImageUpload(file.raw)
        themeForm.value = {
          ...themeForm.value,
          cardBackgroundImages: {
            ...themeForm.value.cardBackgroundImages,
            [status]: imageUrl
          }
        }
        ElMessage.success('Card background image updated')
      } catch (error) {
        if (!error.message?.includes('File too large')) {
          ElMessage.error('Error uploading image')
        }
      } finally {
        uploadLoading.value = false
      }
    }

    const clearBoardImage = () => {
      const newTheme = { 
        ...themeForm.value, 
        boardBackgroundImage: null
      }
      themeForm.value = newTheme
      ElMessage.success('Board background image cleared')
    }

    const clearColumnImage = (status) => {
      const newTheme = {
        ...themeForm.value,
        columnBackgroundImages: {
          ...themeForm.value.columnBackgroundImages,
          [status]: null
        }
      }
      themeForm.value = newTheme
      ElMessage.success('Column background image cleared')
    }

    const clearCardImage = (status) => {
      const newTheme = {
        ...themeForm.value,
        cardBackgroundImages: {
          ...themeForm.value.cardBackgroundImages,
          [status]: null
        }
      }
      themeForm.value = newTheme
      ElMessage.success('Card background image cleared')
    }

    return {
      dialogVisible,
      showUnsavedDialog,
      saving,
      activeTab,
      themeForm,
      showDialog,
      handleClose,
      handleSave,
      handleSaveAndClose,
      handleDiscardChanges,
      handleReset,
      handleBoardImageUpload,
      handleColumnImageUpload,
      handleCardImageUpload,
      clearBoardImage,
      clearColumnImage,
      clearCardImage,
      uploadLoading,
      hasUnsavedChanges
    }
  }
}
</script>

<style scoped>
.customize-theme-btn {
  position: fixed;
  bottom: 2rem;
  right: 8rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-section {
  margin-bottom: 2rem;
}

.status-section h3 {
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #eee;
}

.image-upload {
  margin-top: 0.5rem;
  display: flex;
  gap: 1rem;
}

.image-fit-controls,
.image-position-controls {
  margin-top: 0.5rem;
}

.opacity-control {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.opacity-control span {
  display: block;
  margin-bottom: 0.5rem;
  color: #606266;
  font-size: 14px;
}

.preview-images {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.preview-image {
  margin-top: 0.5rem;
  max-width: 200px;
}

.preview-image img {
  width: 100%;
  height: auto;
  border-radius: 4px;
  border: 1px solid #eee;
}

.preview-image small {
  display: block;
  margin-bottom: 0.25rem;
  color: #666;
}

.el-upload {
  width: auto !important;
}

.el-upload-dragger {
  width: auto !important;
}

.image-fit-controls {
  margin: 1rem 0;
}

.image-position-controls {
  margin: 1rem 0;
}

.el-select {
  width: 100%;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.el-form {
  min-height: 400px;
}
</style> 