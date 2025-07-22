<script setup>
    import Header from '@/components/Header.vue'
    import Footer from '@/components/Footer.vue'

</script>

<template>
    <div class="flex flex-col min-h-screen">
        <Header/>
        <RouterView class="grow"></RouterView>
        <Footer/>
    </div>
</template>