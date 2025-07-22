import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import App from '@/App.vue'
import router from '@/router/routes'
import { useAuthStore } from '@/stores/auth'

// アプリケーションを非同期で起動するための関数を定義
async function startApp() {
    console.log('アプリケーションのスタートアップ関数、実行開始。');
    console.log('App.vueをルートコンポーネントとして指定し、Vueアプリケーションのインスタンスを作成しています。');
    const app = createApp(App)

    console.log('Piniaの初期化を行なっています');
    const pinia = createPinia()
    pinia.use(piniaPluginPersistedstate)
    app.use(pinia)

    const authStore = useAuthStore()

    try {
        console.log('authStoreを使い、リフレッシュトークンによるセッションの復元を試みています(非同期、await)');
        await authStore.refreshAccessToken();
        console.log('リフレッシュトークンからセッションの復元が完了しました！');
    } catch (error) {
        // リフレッシュトークンがない、または無効な場合はエラーになるが、
        // プログラムを停止させる必要はない。単に「ログインしていない」状態が確定するだけ。
        console.log('セッションの復元ができませんでした。ゲストユーザーとしてアクセスします。');
    }

    console.log('Vueアプリにルーターをインストールしています。これによりルーターが初期化され、最初のページへのナビゲーションがトリガーされ、beforeEachガードが初めて実行されます。');
    // これで、router.beforeEachが正しい`isAuthenticated`の状態で実行される
    app.use(router)

    console.log('全ての設定が完了したVueアプリケーションインスタンスを、HTML内のid="app"を持つ要素に**マウント（関連付け）**しています。');
    app.mount('#app')

    console.log('アプリケーションのスタートアップ関数終了。')
}


startApp()