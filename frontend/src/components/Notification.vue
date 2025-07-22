<script setup>
    import { useNotificationStore } from '@/stores/notification';
    import { computed } from 'vue';

    import checkIconRaw from '@/assets/icons/success.svg?raw';      // 成功用
    import errorIconRaw from '@/assets/icons/error.svg?raw';      // エラー用 (例: xmark.svgなど)
    import infoIconRaw from '@/assets/icons/info.svg?raw';        // 情報用 (例: info-circle.svgなど)

    import closeIconRaw from '@/assets/icons/close.svg?raw';      // 閉じるボタン用 (例: xmark.svgを流用も可)


    const notificationStore = useNotificationStore();

    const isVisible = computed(() => notificationStore.isVisible);
    const message = computed(() => notificationStore.message);
    const type = computed(() => notificationStore.type);

    const currentIconRaw = computed(() => {
        switch (type.value) {
            case 'success':
                return checkIconRaw;
            case 'error':
                return errorIconRaw;
            case 'info':
                return infoIconRaw;
            default:
                return null;
        }
    });

    const closeNotification = () => {
        notificationStore.hideNotification();
    };

</script>

<template>
    <Transition name="fade">
        <div
            v-if="isVisible"
            class="fixed top-20 right-8 z-50 flex flex-col items-center min-w-[250px] backdrop-blur-xs bg-black/55 p-4 rounded shadow-lg"
        >
            <!-- アイコン -->
            <div v-if="currentIconRaw"
                v-html="currentIconRaw"
                class="[&>svg]:size-12"
                :class="{
                    '[&>svg]:text-teal-400': type==='success',
                    '[&>svg]:text-pink-400': type==='error',
                    '[&>svg]:text-yellow-400': type==='info'
                }"
            ></div>

            <p class="text-white pt-2">
                {{ message }}
            </p>

            <!-- 閉じるボタンのアイコン表示 -->
            <button
                @click="closeNotification"
                class="absolute top-2 right-2 [&>svg]:text-white [&>svg]:size-6.5 cursor-pointer hover:opacity-70"
                v-html="closeIconRaw"
            ></button>

        </div>
    </Transition>
</template>

<style scoped>
    /* 通知の表示/非表示時のトランジション */
    .fade-enter-active,
    .fade-leave-active {
        transition: opacity 0.5s ease;
    }
    .fade-enter-from,
    .fade-leave-to {
        opacity: 0;
    }
</style>