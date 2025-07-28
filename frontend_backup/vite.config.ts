// @ts-check
import { defineConfig } from 'vite';
import reactRefresh from '@vitejs/plugin-react-refresh';
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [reactRefresh()],
  server: {
    port: 3000,
    host: true,
    open: false,
    hmr: { clientPort: 443 } // Fix for Vite HMR
  },
  build: {
    outDir: './dist',
    emptyOutDir: true,
    rollupOptions: {
      input: './src/main.tsx' // Explicit entry point
    }
  },
  css: {
    devSourcemap: true
  },
  resolve: {
    alias: {
      '@': '/src'
    }
  },
  base: './',
  optimizeDeps: {
    include: ['react', 'react-dom']
  }
});
