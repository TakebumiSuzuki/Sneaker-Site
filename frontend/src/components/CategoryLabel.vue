<script setup>
    import { computed } from 'vue'

    const props = defineProps({
        label: String
    })

    const labelColor = computed(() => {
        switch (props.label) {
            case 'running':
                return 'bg-indigo-400'
            case 'training':
                return 'bg-teal-400'
            case 'basketball':
                return 'bg-yellow-400'
            case 'lifestyle':
                return 'bg-purple-400'
            default:
            return ''
        }
    })
</script>


<template>
    <div class="absolute top-1.5 right-1.5 text-white  px-2 rounded text-sm leading-relaxed opacity-90" :class="labelColor">
        {{ props.label }}
    </div>
</template>