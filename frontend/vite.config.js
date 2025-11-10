import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { copyFileSync } from 'fs'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    {
      name: 'copy-pwa-files',
      buildStart() {
        // Copy service worker and manifest to public during build
        try {
          copyFileSync(
            resolve(__dirname, 'public/service-worker.js'),
            resolve(__dirname, 'dist/service-worker.js')
          )
          copyFileSync(
            resolve(__dirname, 'public/manifest.json'),
            resolve(__dirname, 'dist/manifest.json')
          )
        } catch (err) {
          console.warn('PWA files not found, skipping copy')
        }
      }
    }
  ],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  publicDir: 'public',
})

