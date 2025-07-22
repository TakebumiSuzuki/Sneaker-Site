import { ref, computed } from "vue";
import { defineStore } from "pinia";
import apiClient from "@/api";


export const useAuthStore = defineStore("auth", () => {

    // --- state ---
    const accessToken = ref(null);
    const user = ref(null);

    // --- getters ---
    // !accessToken.value をすると、「accessToken.value が truthy（存在する値）なら false、
    // falsy（null や undefined、空文字列など）なら true」になります。
    // さらにもう一度 ! をかけた !!accessToken.value は、その逆を取る
    const isAuthenticated = computed(() => !!accessToken.value);

    const isAdmin = computed(() => user.value?.is_admin ?? false)

    // 共通のクライアント側ログアウト処理
    function clearClientAuthState() {
        accessToken.value = null;
        user.value = null;
    }

    // --- actions ---
    async function changeUsername(newUsername) {
        try {
            // 分割代入は、オブジェクトの中から自分が必要なプロパティだけを名前を指定して取り出すための構文です。
            const { data } = await apiClient.patch(
                // user.value.id と書くことで、この大前提が崩れた瞬間に TypeError という形でプログラムをクラッシュ（停止）
                // させることができます。user.value?.idと書いてしまうとバグをすぐに特定できない。
                `/api/users/${user.value.id}/username`,
                { username: newUsername }
            );
            user.value = data.user_data;

        } catch (err) {
            console.error("Failed to change Username.", err);
            // もし?.の左側が null または undefined なら、そこで処理を中断して undefined を返す。
            // 最後のmessageはサーバーから送られるjsonのキー。それ以前はaxiosのエラーオブジェクトの構造。
            const errorMessage = err.response?.data?.message || "不明なエラーが発生しました。";
            throw new Error(errorMessage);
        }
    }

    async function changePassword(oldPassword, newPassword) {
        try {
            await apiClient.patch(
                `/api/users/${user.value.id}/password`,
                {
                    old_raw_password: oldPassword,
                    new_raw_password: newPassword,
                }
            );
            clearClientAuthState();

        } catch (err) {
            console.error("Failed to change password.", err);
            const errorMessage = err.response?.data?.message || "不明なエラーが発生しました。";
            throw new Error(errorMessage);
        }
    }

    async function login(email, password) {
        try {
            // { email, password } はjsの省略記法で、{ email: email, password: password }と同じ。
            // デフォルトで、axios.postにオブジェクトを渡せば、自動的に JSON.stringify され、さらに
            // Content-Type: application/json ヘッダーで送信される

            // {withCredentials: true} は、以下の両方の動作を有効にします。(サーバーがCORSに対応しているという前提で、さらに、)
            // 1. リクエスト時: ブラウザに保存されている、そのドメインに関連するクッキーを自動的にリクエストに添付して送信する。
            // 2. レスポンス時: サーバーからのレスポンスヘッダーに含まれる Set-Cookie を解釈し、ブラウザにクッキーを保存する。
            // この2つはセットであり、フロントエンドのコードで片方だけを有効にすることはできません。
            // ここでは、サーバーからのリフレッシュトークンを、サーバーの指示通りにクッキーとしてブラウザに保存させるために記述。
            const { data } = await apiClient.post(
                "/api/users/login",
                { email: email, raw_password: password },
                { withCredentials: true }
            );
            accessToken.value = data.access_token; //これと同時にrefresh tokenの方はクッキーに保存される
            user.value = data.user_data;
            return user.value;

        } catch (err) {
            clearClientAuthState(); // 失敗時もクリア
            console.error("Failed to login.", err);
            const errorMessage = err.response?.data?.message || "不明なエラーが発生しました。";
            throw new Error(errorMessage);
        }
    }

    async function logout() {
        try {
            // { withCredentials: true }をつけているのは、サーバー側でrefresh tokenをブラックリストにするため。
            // また、その後、サーバーからのレスポンスにより、クライアント側のクッキー内のrefresh tokenも消す。
            await apiClient.post(
                "/api/users/logout",
                {},
                { withCredentials: true }
            );
        } catch (err) {

            if (err.response) {
                // サーバーからレスポンスが返ってきた場合 (4xx, 5xxエラー)
                console.error("Status:", err.response.status); // 例: 401
                console.error("Data:", err.response.data);   // 例: { message: "...", error_code: "..." }
                console.error("Headers:", err.response.headers);
            } else if (err.request) {
                // リクエストはしたが、サーバーからレスポンスがなかった場合 (ネットワークエラーなど)
                console.error("No response received:", err.request);
            } else {
                // リクエストの設定時にエラーが発生した場合
                console.error("Error setting up request:", err.message);
            }

            // サーバー側のログアウトに失敗しても、ユーザー体験としては問題ないことが多い。
            // エラーをコンソールに出力するだけで、処理を続行させる。
            // ここでエラーを再スローしないことで、finallyブロックの後に処理が続くことを保証する。
            console.error(
                "Server-side logout failed, but proceeding with client-side logout.",
                err
            );
        } finally {
            clearClientAuthState();
        }
    }

    async function deleteUser(user_id) {
        try {
            await apiClient.delete(`/api/users/${user_id}`);
            clearClientAuthState();

        } catch (err) {
            console.error("Failed to delete user on the server.", err);
            const errorMessage = err.response?.data?.message || "アカウントの削除に失敗しました。時間をおいて再度お試しください。";
            // エラーを再スローして、呼び出し元に処理の失敗を伝える
            throw new Error(errorMessage);
        }
    }

    // この関数が呼び出されるシナリオは主に2つ
    // 1. アプリ起動時のセッション復元
    // 2. Axiosレスポンスインターセプター：APIリクエストが「401 Unauthorized（アクセストークン切れ）」で失敗した時
    async function refreshAccessToken() {
        try {
            console.log('これからrefreshのエンドポイントにリクエストを送ります。{ withCredentials: true }とし、refreshTokenを送ります')
            const { data } = await apiClient.post(
                "/api/users/refresh",
                {},
                { withCredentials: true }
            );
            accessToken.value = data.access_token;
            if (data.user_data) {
                user.value = data.user_data;
            }
            // インターセプターが、この return された new_access_token を使う
            return data.access_token;

        } catch (err) {
            console.error("Failed to refresh token. Logging out.", err);
            // リフレッシュ失敗時はログアウト
            await logout();
            // エラーを再スローして、元のAPI呼び出しが失敗したことを伝える
            throw err;
        }
    }


    return {
        accessToken,
        user,
        isAuthenticated,
        isAdmin,
        changeUsername,
        changePassword,
        login,
        refreshAccessToken,
        logout,
        deleteUser,
    };
}, {
    // 3. ここに永続化の設定を追加します
    persist: true,
});
