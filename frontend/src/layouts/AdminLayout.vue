<script setup>
    import Header from '@/components/Header.vue'

</script>


<template>
    <div class="flex flex-col min-h-screen">
        <Header/>
        <div class="text-center text-neutral-50 bg-red-600/80 py-1">Admin Mode</div>
        <RouterView class="grow"></RouterView>
    </div>
</template>