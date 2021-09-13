import { useEffect, useState } from 'react';

export const useDarkMode = () => {
  const [theme, setTheme] = useState('day');

  const today = new Date();
  const hour = today.getHours();

  useEffect(() => {
    if (hour > 17) {
      setTheme('night');
    } else {
      setTheme('day');
    }
  }, [hour]);

  return [theme];
};
