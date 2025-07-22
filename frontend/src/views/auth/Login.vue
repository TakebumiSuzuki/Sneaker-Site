<script setup>
    import { reactive, ref } from 'vue';
    import { useAuthStore } from '@/stores/auth';
    import { useRouter } from 'vue-router';
    import { useNotificationStore } from '@/stores/notification';

    import AuthBgWrapper from '@/components/AuthBgWrapper.vue';
    import pickup3 from '@/assets/images/pickup3.jpg'
    import Loading from '@/components/icons/Loading.vue'

    const authStore = useAuthStore()
    const router = useRouter()
    const notificationStore = useNotificationStore();

    const loading = ref(false)

    const formData = reactive({
        email: null,
        password: null}
    )
    const errors = reactive({
        serverErrors: null,
        email: null,
        password: null
    })

    const handleSubmit = async ()=>{
        errors.email = null
        errors.password = null
        errors.serverErrors = null

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!formData.email){
            errors.email = 'Enter email address.'
        } else if (formData.email.length < 3 || formData.email.length > 255 || !emailRegex.test(formData.email)) {
            errors.email = 'Enter correct email.'
        }
        if (!formData.password){
            errors.password = 'Enter password'
        } else if (formData.password.length<7  || formData.password.length > 40){
            errors.password = 'Enter correct password'
        }
        if (errors.email || errors.password) { return }; // APIリクエストに進ませない

        try{
            loading.value = true
            await authStore.login(formData.email, formData.password);
            notificationStore.showNotification('Login successful!', 'success');
            console.log(`アクセストークン: ${authStore.accessToken}`)
            console.log(`ユーザーデーター: ${authStore.user.username}`)
            router.push({name:'home'})
        }catch(err){
            notificationStore.showNotification('Failed to login', 'error');
            errors.serverErrors = err.message
            formData.password = null
        }finally{
            loading.value = false
        }
    }

</script>


<template>
    <AuthBgWrapper :backgroundImageUrl="pickup3">
        <slot>
            <div class="text-4xl pt-12 text-center tracking-wide">Welcome Back!</div>

            <form @submit.prevent="handleSubmit" class="pt-10 pb-14" novalidate>
                <p class="text-center text-red-500 text-sm" v-if="errors.serverErrors">{{ errors.serverErrors }}</p>

                <label for="email-field" class="sr-only">Email</label>
                <p class="text-right text-red-500 text-sm" v-if="errors.email">{{ errors.email }}</p>
                <input
                    id="email-field"
                    class="border rounded-lg block py-2 px-3 w-full mb-8 shadow-sm outline-none border-neutral-400 focus:border-neutral-600 focus:bg-white/10 focus:shadow-md"
                    type="email"
                    placeholder="Email"
                    v-model.trim="formData.email"
                >
                <label for="password-field" class="sr-only">Password</label>
                <p class="text-right text-red-500 text-sm" v-if="errors.password">{{ errors.password }}</p>
                <input
                    id="password-field"
                    class="border rounded-lg block py-2 px-3 w-full mb-8 shadow-sm outline-none border-neutral-400 focus:border-neutral-600 focus:bg-white/10 focus:shadow-md"
                    type="password"
                    placeholder="Password"
                    v-model="formData.password"
                >

                <button
                    type="submit"
                    class="text-lg text-white px-6 py-2 rounded-lg bg-gradient-to-br from-teal-500 to-teal-600 w-full mb-4 shadow-sm cursor-pointer disabled:bg-neutral-700 disabled:cursor-not-allowed hover:from-teal-600 hover:to-teal-700 active:from-teal-700 active:to-teal-800 transition ease-in-out hover:shadow-lg active:shadow-xl"
                    :disabled="loading"
                >
                    <div v-if="loading" class="flex gap-2 items-center justify-center">
                        <Loading class="animate-spin size-4.5"/>
                        Processing
                    </div>
                        <div v-else>Login</div>
                </button>

                <p class="text-right">
                    you don't have
                    <RouterLink :to="{name: 'register'}">
                        <span class="text-teal-700 font-bold relative hover:after:bg-teal-600 hover:after:left-0 hover:after:right-0 hover:after:bottom-0 hover:after:h-[2px] after:absolute after:origin-center after:scale-x-0 hover:after:scale-x-100 after:transition">account</span>
                    </RouterLink>
                    yet?&nbsp;&nbsp;&nbsp;
                </p>
            </form>

        </slot>

    </AuthBgWrapper>


</template>