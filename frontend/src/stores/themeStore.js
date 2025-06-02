import { ref } from 'vue';
import { ThemeService } from '../services/api';

const defaultTheme = {
  boardBackground: 'linear-gradient(to bottom, #1a1a2e, #16213e)',
  boardBackgroundImage: null,
  boardImageFit: 'cover', // cover, contain, or custom
  boardImagePosition: 'center center',
  columnBackgrounds: {
    ON_HOLD: 'rgba(244, 244, 244, 0.1)',
    CURRENT: 'rgba(255, 255, 255, 0.1)',
    UPCOMING: 'rgba(255, 255, 255, 0.1)',
    COMPLETED: 'rgba(240, 255, 240, 0.1)',
  },
  columnOpacity: {
    ON_HOLD: 0.1,
    CURRENT: 0.1,
    UPCOMING: 0.1,
    COMPLETED: 0.1,
  },
  columnBackgroundImages: {
    ON_HOLD: null,
    CURRENT: null,
    UPCOMING: null,
    COMPLETED: null,
  },
  columnImageFit: {
    ON_HOLD: 'cover',
    CURRENT: 'cover',
    UPCOMING: 'cover',
    COMPLETED: 'cover',
  },
  columnImagePosition: {
    ON_HOLD: 'center center',
    CURRENT: 'center center',
    UPCOMING: 'center center',
    COMPLETED: 'center center',
  },
  cardBackgrounds: {
    ON_HOLD: 'rgba(255, 255, 255, 0.95)',
    CURRENT: 'rgba(255, 255, 255, 0.95)',
    UPCOMING: 'rgba(255, 255, 255, 0.95)',
    COMPLETED: 'rgba(255, 255, 255, 0.95)',
  },
  cardBackgroundImages: {
    ON_HOLD: null,
    CURRENT: null,
    UPCOMING: null,
    COMPLETED: null,
  },
  cardImageFit: {
    ON_HOLD: 'cover',
    CURRENT: 'cover',
    UPCOMING: 'cover',
    COMPLETED: 'cover',
  },
  cardImagePosition: {
    ON_HOLD: 'center center',
    CURRENT: 'center center',
    UPCOMING: 'center center',
    COMPLETED: 'center center',
  },
  cardOpacity: {
    ON_HOLD: 0.95,
    CURRENT: 0.95,
    UPCOMING: 0.95,
    COMPLETED: 0.95,
  },
  columnTitleColors: {
    ON_HOLD: '#fff',
    CURRENT: '#fff',
    UPCOMING: '#fff',
    COMPLETED: '#fff',
  }
};

export const useThemeStore = () => {
  const currentTheme = ref(structuredClone(defaultTheme));
  const loading = ref(false);
  const error = ref(null);

  const updateTheme = async (newTheme) => {
    loading.value = true;
    error.value = null;
    
    try {
      // Ensure all required properties exist
      const updatedTheme = {
        boardBackground: newTheme.boardBackground || defaultTheme.boardBackground,
        boardBackgroundImage: newTheme.boardBackgroundImage,
        boardImageFit: newTheme.boardImageFit || defaultTheme.boardImageFit,
        boardImagePosition: newTheme.boardImagePosition || defaultTheme.boardImagePosition,
        columnBackgrounds: { ...defaultTheme.columnBackgrounds, ...newTheme.columnBackgrounds },
        columnOpacity: { ...defaultTheme.columnOpacity, ...newTheme.columnOpacity },
        columnBackgroundImages: { ...defaultTheme.columnBackgroundImages, ...newTheme.columnBackgroundImages },
        columnImageFit: { ...defaultTheme.columnImageFit, ...newTheme.columnImageFit },
        columnImagePosition: { ...defaultTheme.columnImagePosition, ...newTheme.columnImagePosition },
        cardBackgrounds: { ...defaultTheme.cardBackgrounds, ...newTheme.cardBackgrounds },
        cardBackgroundImages: { ...defaultTheme.cardBackgroundImages, ...newTheme.cardBackgroundImages },
        cardImageFit: { ...defaultTheme.cardImageFit, ...newTheme.cardImageFit },
        cardImagePosition: { ...defaultTheme.cardImagePosition, ...newTheme.cardImagePosition },
        cardOpacity: { ...defaultTheme.cardOpacity, ...newTheme.cardOpacity },
        columnTitleColors: { ...defaultTheme.columnTitleColors, ...newTheme.columnTitleColors }
      };
      
      const response = await ThemeService.updateTheme(updatedTheme);
      currentTheme.value = response.data;
    } catch (err) {
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const loadTheme = async () => {
    loading.value = true;
    error.value = null;
    
    try {
      const response = await ThemeService.getCurrentTheme();
      if (response.data) {
        currentTheme.value = response.data;
      }
    } catch (err) {
      error.value = err.message;
      console.error('Error loading theme:', err);
      // If we can't load the theme, use default
      currentTheme.value = structuredClone(defaultTheme);
    } finally {
      loading.value = false;
    }
  };

  const resetTheme = async () => {
    loading.value = true;
    error.value = null;
    
    try {
      await ThemeService.resetTheme();
      currentTheme.value = structuredClone(defaultTheme);
    } catch (err) {
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Load theme from backend on initialization
  loadTheme();

  return {
    currentTheme,
    updateTheme,
    resetTheme,
    loading,
    error
  };
}; 