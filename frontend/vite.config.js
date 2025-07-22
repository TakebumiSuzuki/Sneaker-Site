import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },

  server: { // ← serverオブジェクトを追加または編集
    proxy: {
      // '/api'という文字列で始まるリクエストをプロキシの対象にする
      '/api': {
        // 転送先となるAPIサーバーのURLを指定
        target: 'http://127.0.0.1:5000',

        // サーバーのオリジンを偽装するために必要
        changeOrigin: true,

        // オプション：もしFlask側で/apiというプレフィックスが不要な場合
        // 例えば、Flaskのルートが /users/login の場合、
        // /api/users/login を /users/login に書き換える
        // rewrite: (path) => path.replace(/^\/api/, ''),
      }
    }
  }
})
