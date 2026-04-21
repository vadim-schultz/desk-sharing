import { Button } from '@chakra-ui/react';
import { FaMoon, FaSun } from 'react-icons/fa';

import { useColorMode } from '../ui/color-mode';

const ColorModeToggle = () => {
  const { colorMode, toggleColorMode } = useColorMode();

  return (
    <Button
      aria-label="Toggle color mode"
      onClick={toggleColorMode}
      variant="ghost"
      size="sm"
      colorPalette="gray"
    >
      {colorMode === 'light' ? <FaMoon /> : <FaSun />}
    </Button>
  );
};

export default ColorModeToggle;
