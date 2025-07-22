import { ref } from 'vue';
import { defineStore } from 'pinia';

export const useNotificationStore = defineStore('notification', () => {
    // --- State (リアクティブな状態) ---
    const isVisible = ref(false);

    const message = ref(null);
    const type = ref(null); // 'success', 'error', 'info' など
    const timeoutId = ref(null); // 通知を自動で消すためのタイマーID

    // --- Actions (状態を変更する関数) ---
    const showNotification = (msg, msgType = 'info', duration = 7000) => {
        // 既にタイマーが設定されている場合はクリア
        if (timeoutId.value) {
            clearTimeout(timeoutId.value);
        }

        message.value = msg;
        type.value = msgType;
        isVisible.value = true;

        // 指定時間後に通知を非表示にする
        timeoutId.value = setTimeout(() => {
            hideNotification(); // 直接関数を呼び出し
        }, duration);
    };

    const hideNotification = () => {
        isVisible.value = false;
        message.value = null;
        type.value = null;
        if (timeoutId.value) {
            clearTimeout(timeoutId.value);
            timeoutId.value = null;
        }
    };


    return {
        message,
        type,
        isVisible,
        showNotification,
        hideNotification,
        // timeoutId は内部的に使うだけなので、通常は公開しない
    };
});