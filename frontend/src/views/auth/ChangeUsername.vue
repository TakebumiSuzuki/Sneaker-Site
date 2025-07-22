<script setup>
    import { reactive, ref } from 'vue';
    import { useAuthStore } from '@/stores/auth';
    import { useRouter } from 'vue-router'
    import { useNotificationStore } from '@/stores/notification';

    import AuthBgWrapper from '@/components/AuthBgWrapper.vue';
    import pickup2 from '@/assets/images/pickup2.jpg'
    import Check from '@/components/icons/Check.vue'
    import Loading from '@/components/icons/Loading.vue'

    const notificationStore = useNotificationStore();
    const authStore = useAuthStore()
    const router = useRouter()

    const loading = ref(false)

    const formData = reactive({
        username: authStore.user?.username
    })
    const errors = reactive({
        serverErrors: null,
        username: null,
    })

    const handleSubmit = async ()=>{
        errors.username = null
        errors.serverErrors = null

        if (!formData.username){
            errors.username = 'Enter username.'
        } else if (formData.username.length < 2) {
            errors.username = 'Username should be more than 2 charactors'
        } else if (formData.username.length > 30){
            errors.username = 'Username is too long.'
        }

        if (errors.username) { return }; // APIリクエストに進ませない

        try{
            loading.value = true
            await authStore.changeUsername(formData.username);
            notificationStore.showNotification('Username updated successfully.', 'success');
            router.push({name:'home'})
        }catch(err){
            notificationStore.showNotification('Failed to update username', 'error');
            errors.serverErrors = err.message
        }finally{
            loading.value = false
        }
    }

</script>


<template>
    <AuthBgWrapper :backgroundImageUrl="pickup2">
        <div>
            <div class="text-4xl pt-12 text-center tracking-wide">
                Change Username
            </div>

            <form @submit.prevent="handleSubmit" class="pt-10 pb-14" novalidate>
                <p class="text-center text-red-500 text-sm" v-if="errors.serverErrors">{{ errors.serverErrors }}</p>

                <label for="username-field" class="sr-only">Username</label>
                <p class="text-right text-red-500 text-sm" v-if="errors.username">{{ errors.username }}</p>
                <input
                    id="username-field"
                    class="border rounded-lg block py-2 px-3 w-full mb-8 shadow-sm outline-none border-neutral-400 focus:border-neutral-600 focus:bg-white/10 focus:shadow-md"
                    type="text"
                    placeholder="New Username"
                    v-model.trim="formData.username"
                >

                <button
                    type="submit"
                    class="text-lg text-white px-6 py-2 rounded-lg bg-gradient-to-br from-indigo-400 to-indigo-500 w-full mb-4 shadow-sm cursor-pointer disabled:bg-neutral-600 disabled:cursor-not-allowed hover:from-indigo-500 hover:to-indigo-600 active:from-indigo-600 active:to-indigo-700 transition ease-in-out hover:shadow-lg active:shadow-xl opacity-90"
                    :disabled="loading"
                >
                    <div v-if="loading" class="flex gap-2 items-center justify-center">
                        <Loading class="animate-spin size-4.5"/>
                        Processing...
                    </div>
                    <div v-else class="flex gap-2 items-center justify-center">
                        <Check class="size-4.5"/>
                        Change Username
                    </div>
                </button>

            </form>

        </div>

    </AuthBgWrapper>


</template>