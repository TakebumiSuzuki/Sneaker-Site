<script setup>
    import PublicLayout from '@/layouts/PublicLayout.vue'

</script>

<template>
    <div class="px-2 md:px-4 py-12 ">
        <div class="flex items-center justify-center">
            <div class="w-full max-w-md rounded-xl bg-white p-8 text-center shadow-lg">
                <h1 class="mb-4 text-4xl font-bold text-gray-800">
                    Access Denied
                </h1>
                <p class="mb-8 text-lg text-gray-600">
                    You do not have the required administrator privileges to view this page.
                </p>
                <router-link
                    to="/"
                    class="inline-block rounded-md bg-indigo-400 px-6 py-2 font-semibold text-white transition-colors hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                >
                    Back to Home
                </router-link>
            </div>
        </div>
    </div>
</template>

