import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

const IGNORED_PROXY_ERROR_CODES = new Set(['ECONNRESET', 'ECONNABORTED', 'EPIPE'])

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    typescript: {
      ignoreBuildErrors: true,
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
        configure: (proxy) => {
          proxy.removeAllListeners('error')
          proxy.on('error', (err) => {
            const code = (err as NodeJS.ErrnoException).code
            if (code && IGNORED_PROXY_ERROR_CODES.has(code)) return
            console.error('[vite] ws proxy error:', err.message)
          })
        },
      },
    },
  },
})