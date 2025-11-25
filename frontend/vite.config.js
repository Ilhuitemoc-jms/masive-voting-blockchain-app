import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  
  server: {
    port: 5173,
    host: '0.0.0.0',
    proxy: {
      // Proxy para el backend Django
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    }
  },
  
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: true
  }
})
