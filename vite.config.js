import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/auth': 'http://localhost:8000',
      '/questions': 'http://localhost:8000',
      '/exam': 'http://localhost:8000',
      '/dashboard': 'http://localhost:8000',
      '/resources': 'http://localhost:8000',
    }
  }
})
export default defineConfig({
  base: "/smart-exam-preparation-project/",
  plugins: [react()],
});
