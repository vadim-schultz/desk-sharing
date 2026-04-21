import globals from 'globals';
import pluginJs from '@eslint/js';
import tseslint from 'typescript-eslint';
import pluginReactConfig from 'eslint-plugin-react/configs/recommended.js';
import pluginReactHooks from 'eslint-plugin-react-hooks';
import pluginReactRefresh from 'eslint-plugin-react-refresh';
import prettierConfig from 'eslint-config-prettier';

export default [
  {
    ignores: ['dist', 'node_modules', '*.js'],
  },
  pluginJs.configs.recommended,

  ...tseslint.configs.recommended,
  {
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        ecmaFeatures: { jsx: true },
        sourceType: 'module',
        project: ['./tsconfig.json'],
      },
      globals: {
        ...globals.browser,
        ...globals.es2020,
      },
    },
    files: ['src/**/*.{ts,tsx}'],
    plugins: {
      'react-hooks': pluginReactHooks,
      'react-refresh': pluginReactRefresh,
    },
    rules: {
      'react-refresh/only-export-components': 'warn',
    },
  },

  {
    ...pluginReactConfig,
    files: ['src/**/*.{ts,tsx}'],
    settings: {
      react: {
        version: 'detect',
      },
    },
    rules: {
      'react/jsx-uses-react': 'off',
      'react/react-in-jsx-scope': 'off',
    },
  },

  {
    files: ['src/**/*.{ts,tsx}'],
    plugins: {
      'react-hooks': pluginReactHooks,
    },
    rules: {
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
    },
  },

  prettierConfig,
];
