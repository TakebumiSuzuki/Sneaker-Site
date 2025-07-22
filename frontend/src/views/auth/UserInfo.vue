<script setup>
    import { computed } from 'vue';
    import { useRouter } from 'vue-router';
    import { useAuthStore } from '@/stores/auth';
    import { useNotificationStore } from '@/stores/notification';
    import { useAlertStore } from '@/stores/alert';

    import AuthBgWrapper from '@/components/AuthBgWrapper.vue';
    import pickup2 from '@/assets/images/pickup2.jpg'
    import User from '@/components/icons/User.vue'
    import Password from '@/components/icons/Password.vue'
    import Delete from '@/components/icons/Delete.vue'

    const notificationStore = useNotificationStore();
    const alertStore = useAlertStore()
    const auth = useAuthStore()
    const router = useRouter()

    const username = computed(() => auth.user?.username)
    const email = computed(() => auth.user?.email)
    const userInfoExists = computed(() => !!auth.user)


    const handleDeleteButton = async()=>{
        try{
            const result = await alertStore.showAlert(
                "Are you sure you want to delete your account?",
                [
                    { text: 'Cancel', value: false, style: 'primary' },
                    { text: 'Yes', value: true, style: 'secondary' }
                ],
                {overlayClickToClose: true}
            )
            if (result){
                console.log('yes')
                deleteUser()
            }else{
                console.log('cancel')
            }
        }catch{
            console.log('画面外クリックキャンセル')
        }
    }

    async function deleteUser(){
        if (auth.user){
            try{
                await auth.deleteUser(auth.user.id)
                notificationStore.showNotification('Your accout was deleted.', 'success');
                router.push({name: 'home'})
            }catch(err){
                console.log(err)
                notificationStore.showNotification('Failed to delete your account', 'error');
            }

        }else{
            // auth.user が存在しない場合のハンドリング
            alert('ユーザー情報がありません。');
            router.push({ name: 'login' }); // ログインページにリダイレクトするなど
        }
    }

</script>


<template>
    <AuthBgWrapper :backgroundImageUrl="pickup2">
        <div>
            <div class="text-4xl pt-12 pb-10 text-center tracking-wide ">
                Manage Your Account
            </div>

            <div v-if="userInfoExists" class="pb-10">
                <div class="flex flex-col gap-4 items-center text-xl pb-10">
                    <p>Username: {{ username }}</p>
                    <p>Email: {{ email }}</p>
                </div>

                <RouterLink
                    :to="{name:'change-username'}"
                    class="text-lg text-white text-center py-2 rounded-lg bg-gradient-to-br from-indigo-400 to-indigo-500 w-full mb-6 shadow-sm cursor-pointer hover:from-indigo-500 hover:to-indigo-600 active:from-indigo-600 active:to-indigo-700 transition ease-in-out hover:shadow-lg active:shadow-xl opacity-90 flex gap-2 justify-center items-center">
                    <User class="size-5"/>
                    Change Username
                </RouterLink>

                <RouterLink
                    :to="{name:'change-password'}"
                    class="text-lg text-white text-center py-2 rounded-lg bg-gradient-to-br from-teal-500 to-teal-600 w-full mb-6 shadow-sm cursor-pointer  hover:from-teal-600 hover:to-teal-700 active:from-teal-700 active:to-teal-800 transition ease-in-out hover:shadow-lg active:shadow-xl opacity-90 flex gap-2 justify-center items-center"
                >
                    <Password class="size-5"/>
                    Change Password
                </RouterLink>

                <button
                    type="button"
                    @click="handleDeleteButton"
                    class="text-lg text-white text-center py-2 rounded-lg bg-gradient-to-br from-pink-500 to-pink-600 w-full mb-6 shadow-sm cursor-pointer  hover:from-pink-600 hover:to-pink-700 active:from-pink-700 active:to-pink-800 transition ease-in-out hover:shadow-lg active:shadow-xl opacity-90 flex gap-2 justify-center items-center"
                >
                    <Delete class="size-5"/>
                    Delete Account
                </button>

            </div>

            <div v-else class="pb-10 text-center text-lg">
                There is no info about you. Please login again.
            </div>
        </div>

    </AuthBgWrapper>

</template>