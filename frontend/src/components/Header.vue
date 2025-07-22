<script setup>
    import { computed } from 'vue';
    import { useAuthStore } from '@/stores/auth';
    import { useNotificationStore } from '@/stores/notification';
    import Logo from '@/components/icons/Logo.vue'
    import { useRouter } from 'vue-router'
    import { useAlertStore } from '@/stores/alert'
    import User from '@/components/icons/User.vue'

    const auth = useAuthStore()
    const notificationStore = useNotificationStore()
    const router = useRouter()
    const alert = useAlertStore()

    const username = computed(() => auth.user?.username)
    const is_admin = computed(()=> auth.user?.is_admin)

    const handleLogout = async()=>{
        // resultには、value、つまりこの場合trueまたは、falseが入る。または、rejectでエラーになる(が、何もしない)
        try {
            const result = await alert.showAlert(
                'Are you sure you want to log out?',
                [{ text: 'Yes', value: true, style: 'primary' }, { text: 'Cancel', value: false, style: 'secondary' }]
            );

            if (result) {
                await auth.logout();
                notificationStore.showNotification('You have been logged out.');
                router.push({ name: 'home' });
            }
            // resultがfalseの場合（例：Cancelボタンが押された場合）、何もせずに正常終了します。

        } catch (error) {
            // Promiseがrejectされた場合（背景クリックや別のアラートによるキャンセルなど）に、このcatchブロックが実行されます。
            // 実際はエラーではないので、何もしなくて良い。一応、consoleに以下のようにログを出すようにしておく
            console.log('Alert was dismissed:', error.message);
        }
    }
</script>

<template>
    <header>
        <div class="px-8 py-3 md:py-4 shadow-md bg-neutral-700 text-neutral-100 text-sm md:text-base">
            <div class="flex flex-col md:flex-row md:justify-between items-center gap-1">
                <div>
                    <RouterLink :to="{name: 'home'}" class="cursor-pointer">
                        <Logo class="w-[180px]"></Logo>
                    </RouterLink>
                </div>
                <div class="max-md:w-full">
                    <div v-if="username" class="flex items-center justify-between gap-6 " >
                        <div v-if="is_admin">
                            <RouterLink :to="{name: 'admin-items'}" class="text-red-400 hover:opacity-80">
                                Admin Home
                            </RouterLink>
                        </div>

                        <div class="">
                            <RouterLink :to="{name: 'user-info'}" class="hover:opacity-80 flex gap-0.5 items-center transition ease-in-out">
                                <User class="size-5"/>
                                {{username}}
                            </RouterLink>
                        </div>


                        <button type="button" @click="handleLogout" class="hover:underline hover:underline-offset-2 hover:opacity-80">
                            Logout
                        </button>
                    </div>

                    <div v-else class="flex items-center justify-between gap-8">
                        <div>
                            <RouterLink :to="{name: 'login'}" class="hover:underline hover:underline-offset-4 hover:opacity-80">
                                Login
                            </RouterLink>
                        </div>
                        <div>
                            <RouterLink :to="{name: 'register'}" class="hover:underline hover:underline-offset-4 hover:opacity-80">
                                Sign Up
                            </RouterLink>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </header>

</template>