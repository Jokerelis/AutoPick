
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath } from 'node:url';

export default defineConfig(({ mode }) => {
  const projectRoot = fileURLToPath(
    new URL('../', import.meta.url)
  );

  const env = loadEnv(mode, projectRoot, 'AUTOPICK_');

  if (!env.AUTOPICK_KAUNAS_KEY) {
    throw new Error('Missing AUTOPICK_KAUNAS_KEY');
  }

  return {
    plugins: [react()],

    server: {
      host: '127.0.0.1',

      proxy: {
        '/api': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,

          rewrite: (path) => path.replace(/^\/api/, ''),

          headers: {
            'X-API-Key': env.AUTOPICK_KAUNAS_KEY
          }
        }
      }
    }
  };
});
