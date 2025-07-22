<script setup>
    const props = defineProps({
        backgroundImageUrl: {
            type: String, // 型は文字列
            required: true // このプロパティは必須とします（任意の場合はfalse）
        }
    })
</script>


<template>
    <div class="grow relative" :style="{ backgroundImage: `url(${props.backgroundImageUrl})` }">
        <div class="absolute z-10 inset-0 bg-black/20 "></div>
        <div class="absolute z-20 inset-0 flex justify-center items-center px-3 md:px-6">
            <div class="shadow-xl rounded-2xl px-4 md:px-8 max-w-[600px] w-full mx-auto backdrop-blur-sm bg-white/70 size-fit -translate-y-[50px]">
                <slot></slot>
            </div>
        </div>
    </div>
</template>