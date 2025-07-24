import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  // ビルド時のベースパスをFlaskの静的ファイルパスに合わせる
  // これはビルドによって生成される 'dist/index.htmlファイル'の中で、読み込まれるJavaScript（.js）や
  // CSS（.css）ファイルへのパスの先頭に/static/という文字列を追加するための設定です。
  base: '/static/',

  build: { // ★★★ 追加（推奨）★★★
    // ビルド成果物の出力先ディレクトリ
    outDir: 'dist',
    // アセット（JS、CSS、画像など）を格納するサブディレクトリ名
    assetsDir: 'assets',
    // Flask側でアセットのパスを動的に解決したい場合に便利
    manifest: true
  }, // ★★★★★★★★★★★★


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
