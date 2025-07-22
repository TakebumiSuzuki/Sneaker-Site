<script setup>
    import { useRouter } from 'vue-router'

    const router = useRouter()

    const goBack = ()=>{
        router.go(-1)
    }
</script>

<template>
    <!-- flex-growの複雑な仕様により、inline-blockと最後の空のdivがないと幅がいっぱいになってしまう -->
    <div @click="goBack"
        class="relative cursor-pointer hover:opacity-80 group inline-block "
    >
        <div class="py-0.5 ">
            « Go Back
        </div>

        <div class="absolute bottom-0 left-0 right-0 origin-center transition ease-in-out h-[1px] bg-neutral-500 scale-x-0 group-hover:scale-x-100 ">
        </div>
    </div>
    <div></div>

</template>