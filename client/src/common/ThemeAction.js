import { useEffect, useState } from 'react';

export const useDarkMode = () => {
  const [today, setDate] = useState(new Date()); // Save the current date to be able to trigger an update
  const [theme, setTheme] = useState('day');

  const hour = today.getHours();

  useEffect(() => {
    if (hour > 17) {
      setTheme('night');
    } else {
      setTheme('day');
    }
  }, []);

  return [theme];
};
