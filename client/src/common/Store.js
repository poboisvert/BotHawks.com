import { configureStore } from '@reduxjs/toolkit';
import themeReducer from './ThemeSlice';

export default configureStore({
  reducer: {
    theme: themeReducer,
  },
});
