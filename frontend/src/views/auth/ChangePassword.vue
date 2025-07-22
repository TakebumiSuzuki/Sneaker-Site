<script setup>
    import { reactive, ref, onMounted } from 'vue';
    import { useAuthStore } from '@/stores/auth';
    import { useRouter } from 'vue-router'
    import { useNotificationStore } from '@/stores/notification';

    import AuthBgWrapper from '@/components/AuthBgWrapper.vue';
    import pickup2 from '@/assets/images/pickup2.jpg'
    import Loading from '@/components/icons/Loading.vue'
    import Check from '@/components/icons/Check.vue'

    const notificationStore = useNotificationStore();
    const authStore = useAuthStore()
    const router = useRouter()

    const loading = ref(false)

    const formData = reactive({
        old_password: null,
        new_password: null,
        new_password_confirmation: null
    })
    const errors = reactive({
        serverErrors: null,
        old_password: null,
        new_password: null,
        new_password_confirmation: null,
    })

    onMounted(()=>{
        console.log(`アクセストークンchange: ${authStore.accessToken}`)
        console.log(authStore.isAdmin)
        if (authStore.user?.username){
            console.log(authStore.user.username  )
        }
    })

    const handleSubmit = async ()=>{
        for (const key in errors) {
            errors[key] = null;
        }

        if (!formData.old_password){
            errors.old_password = 'Enter current password.'
        }

        if (!formData.new_password){
            errors.new_password = 'Enter password'
        } else if (formData.new_password.length<7  || formData.new_password.length > 40){
            errors.new_password = 'Enter correct password'
        }
        if (!formData.new_password_confirmation){
            errors.new_password_confirmation = 'Enter password'
        } else if (formData.new_password !== formData.new_password_confirmation){
            errors.new_password_confirmation = 'Password and password confirmation do not match.'
        }

        if (errors.old_password || errors.new_password || errors.new_password_confirmation || errors.serverErrors){
            return
        }; // APIリクエストに進ませない

        try{
            loading.value = true
            await authStore.changePassword(formData.old_password, formData.new_password);
            notificationStore.showNotification('Password changed successfully.Please log in to continue.', 'success');
            router.push({name:'login'})
        }catch(err){
            notificationStore.showNotification('Failed to change password', 'error');
            errors.serverErrors = err.message
            console.log(err)
        }finally{
            loading.value = false
        }
    }

</script>


<template>
    <AuthBgWrapper :backgroundImageUrl="pickup2">
        <div>
            <div class="text-4xl pt-12 text-center tracking-wide">
                Change Password
            </div>

            <form @submit.prevent="handleSubmit" class="pt-10 pb-14" novalidate>
                <p class="text-center text-red-500 text-sm" v-if="errors.serverErrors">{{ errors.serverErrors }}</p>

                <label for="oldpassword-field" class="sr-only">Current Password</label>
                <p class="text-right text-red-500 text-sm" v-if="errors.old_password">{{ errors.old_password }}</p>
                <input
                    id="oldpassword-field"
                    class="border rounded-lg block py-2 px-3 w-full mb-8 shadow-sm outline-none border-neutral-400 focus:border-neutral-600 focus:bg-white/10 focus:shadow-md"
                    type="password"
                    placeholder="Enter your current password"
                    v-model.trim="formData.old_password"
                >
                <label for="newpassword-field" class="sr-only">New Password</label>
                <p class="text-right text-red-500 text-sm" v-if="errors.new_password">{{ errors.new_password }}</p>
                <input
                    id="newpassword-field"
                    class="border rounded-lg block py-2 px-3 w-full mb-8 shadow-sm outline-none border-neutral-400 focus:border-neutral-600 focus:bg-white/10 focus:shadow-md"
                    type="password"
                    placeholder="Enter new password"
                    v-model.trim="formData.new_password"
                >

                <label for="confirmation-field" class="sr-only">New Password Confirmation</label>
                <p class="text-right text-red-500 text-sm" v-if="errors.new_password_confirmation">{{ errors.new_password_confirmation }}</p>
                <input
                    id="confirmation-field"
                    class="border rounded-lg block py-2 px-3 w-full mb-8 shadow-sm outline-none border-neutral-400 focus:border-neutral-600 focus:bg-white/10 focus:shadow-md"
                    type="password"
                    placeholder="Enter new password again"
                    v-model.trim="formData.new_password_confirmation"
                >

                <button
                    type="submit"
                    class="text-lg text-white px-6 py-2 rounded-lg bg-gradient-to-br from-teal-500 to-teal-600 w-full mb-4 shadow-sm cursor-pointer disabled:bg-neutral-600 disabled:cursor-not-allowed hover:from-teal-600 hover:to-teal-700 active:from-teal-700 active:to-teal-800 transition ease-in-out hover:shadow-lg active:shadow-xl opacity-90"
                    :disabled="loading"
                >
                    <div v-if="loading" class="flex gap-2 items-center justify-center">
                        <Loading class="animate-spin size-4.5"/>
                        Processing...
                    </div>
                    <div v-else class="flex gap-2 items-center justify-center">
                        <Check class="size-5"/>
                        Change Password
                    </div>
                </button>

            </form>

        </div>

    </AuthBgWrapper>


</template>