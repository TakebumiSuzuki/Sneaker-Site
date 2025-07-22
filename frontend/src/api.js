import axios from "axios";
import { useAuthStore } from "@/stores/auth";

const apiClient = axios.create();

// --- リクエストインターセプター ---
// 全てのリクエストにアクセストークンを付与します。
// use メソッドは、引数として関数（コールバック関数）を受け取り、その関数をインターセプターとして登録します。
apiClient.interceptors.request.use((config) => {
    console.log('Axios Requestインターセプター開始')
    // ちなみに、ストアがまだ作られていない場合、Piniaがその場で自動的に作成してくれます。
    const authStore = useAuthStore();
    // ログアウトとリフレッシュのリクエスト「以外」の場合にだけ、ヘッダーを付与する

    if (
        authStore.isAuthenticated &&
        config.url !== "/api/users/logout" &&
        config.url !== "/api/users/refresh"
    ) {
        console.log('ログイン状態において、logoutとrefresh以外のエンドポイントに対してなので、ヘッダーにaccessTokenを含めます')
        config.headers.Authorization = `Bearer ${authStore.accessToken}`;
    } else {
        console.log('ログイン状態ではない、またはlogoutとrefreshのエンドポイントに対してなので、ヘッダーにaccesss Tokenを含めません。')
        // Authorizationヘッダーを明示的に消す
        // delete config.headers.Authorization;
    }
    console.log('Axios Requestインターセプター終了')
    return config;
});


// --- レスポンスインターセプター ---
// アクセストークンの有効期限切れ (401エラー) を検知し、トークンをリフレッシュして元のリクエストを再試行します。

// 以下の変数は当然、クライアントサイドで保持される変数なので、他クライアントとの競合などは一切関係しない。
let isRefreshing = false;
// failedQueue には、トークンリフレッシュが終わるのを待っている、後続のリクエストたちが入っています。
let failedQueue = [];

const processQueue = (error, token = null) => {
    failedQueue.forEach((prom) => {
        if (error) {
            prom.reject(error);
        } else {
            prom.resolve(token);
        }
    });
    failedQueue = [];
};

// interceptors.response.useは、レスポンスに対するインターセプターで、2つの'関数'を引数に取ることができます。
// axios.interceptors.response.use(成功時の処理を行う関数, エラー時の処理を行う関数)
apiClient.interceptors.response.use(
    (response) => response, //JSでの省略記法であり、これは { return response }　と書くのと同じ

    // APIリクエストがエラーになった際に、自動でアクセストークンを再発行し、失敗したリクエストを再試行するという高度な処理を行っています
    // 具体的には、APIリクエストで認証エラー（401 Unauthorized）が発生したときに、ユーザーに再ログインを強いることなく、
    // 裏側で新しいアクセストークンを取得し、元のリクエストを自動でやり直す
    async (error) => {
        console.log('Axios Responseインターセプター開始。これはエラーコード(200番台以外)となっていることを意味します')
        const originalRequest = error.config;

        console.log("レスポンスのインターセプターでエラーを処理し始めます。オリジナルリクエストは、", originalRequest.url);

        // 401エラー、かつトークンリフレッシュAPIへのリクエストではない、かつ再試行でない場合
        // _retryはaxiosの標準プロパティではなく、開発者が独自に付与する目印です
        if (
            error.response?.data?.error_code === "TOKEN_EXPIRED" &&
            !originalRequest._retry
        ){
            console.log('エラーが条件に合致したので、リフレッシュトークンの組み替えを始めます')
            if (isRefreshing) {
                // 現在リフレッシュ処理中の場合、新しいトークンが発行されるまでリクエストを待機させます
                return new Promise((resolve, reject) => {
                    failedQueue.push({ resolve, reject });
                }).then((token) => {
                    originalRequest.headers["Authorization"] =
                        "Bearer " + token;
                    return apiClient(originalRequest);
                });
            }

            //  JavaScriptでは、オブジェクトが作成された後でも、いつでも自由に新しいプロパティを追加したり、
            // 既存のプロパティを削除したりできます。
            originalRequest._retry = true;
            isRefreshing = true;

            const authStore = useAuthStore();
            try {
                const newAccessToken = await authStore.refreshAccessToken();
                processQueue(null, newAccessToken);
                originalRequest.headers[ "Authorization" ] = `Bearer ${newAccessToken}`;
                return apiClient(originalRequest);

            } catch (refreshError) {
                console.log('リフレッシュトークンによる組み替えの作業が失敗です')
                processQueue(refreshError, null);
                // refreshAccessToken内でログアウト処理が走るので、ここではエラーを投げるだけでOK
                return Promise.reject(refreshError);

            } finally {
                isRefreshing = false;
            }
        }
        return Promise.reject(error);
    }
);

export default apiClient;
