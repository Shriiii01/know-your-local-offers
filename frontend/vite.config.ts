/**
 * Vite configuration for Know Your Local Offers frontend
 * Build tool configuration for React + TypeScript application
 */
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true
  }
})