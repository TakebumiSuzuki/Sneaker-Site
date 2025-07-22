
<script setup>
    import { onMounted, ref, computed } from 'vue';

    import apiClient from '@/api'
    import AdminBgWrapper from '@/components/AdminBgWrapper.vue'
    import TagIcon from '@/components/icons/TagIcon.vue'
    import PriceIcon from '@/components/icons/PriceIcon.vue'
    import Loading from '@/components/icons/Loading.vue'
    import AdminGoBack from '@/components/AdminGoBack.vue';

    const props = defineProps({ id: String })
    const numericId = computed(() => Number(props.id))

    const item = ref(null)
    const isLoading = ref(false)
    const error = ref(null)

    onMounted(async()=>{
        try{
            error.value = null
            isLoading.value = true
            const response = await apiClient.get(`/api/sneakers/${numericId.value}`)
            item.value = response.data
        }catch(err){
            console.log('Failed to load item.', err)
            // ここで、実はアドミンではなかったり、ログインしていなかったりした場合のエラーも扱うことになる。
            // また、存在しない商品IDリクエストを送った場合もここにくる。これらの分岐をして適切なエラーメッセージを書くことが重要
            error.value = 'Failed to load item. Please try again later.'
        }finally{
            isLoading.value = false
        }
    })

</script>


<template>
    <div class="px-4 md:px-8 pb-16 bg-gradient-to-br from-neutral-500 to-neutral-600">
        <div class="w-full max-w-[1200px] mx-auto text-neutral-50">
            <div class="max-w-[900px] mx-auto">
                <AdminGoBack class="max-w-[900px] w-full mx-auto"/>
            </div>
            <div v-if="isLoading">
                <Loading class="animate-spin text-sky-400 size-14 mx-auto mt-12"></Loading>
            </div>

            <div v-else-if="error" class="text-center py-12">
                {{ error }}
            </div>

            <div v-else-if="!item" class="text-center py-12">
                There is no data found for this item.
            </div>

            <div v-else class="py-6 w-full">


                <div class="text-4xl tracking-wide pb-4 md:pb-10 text-center">
                        {{ item.name }}
                </div>

                <div class="md:w-full md:flex md:items-sart md:gap-10 max-w-[900px] mx-auto md:mt-8">
                    <div class="w-1/2 mx-auto mb-10">
                        <img :src="item.image_url" alt="" >
                    </div>


                    <div class="w-[80%] mx-auto md:w-1/2 space-y-8">
                        <!-- Description -->
                        <div>
                            <h3 class="text-xl font-bold mb-2">Description</h3>
                            <p class=" leading-relaxed">{{ item.description }}</p>
                        </div>

                        <!-- Specifications -->
                        <div>
                            <h3 class="text-xl font-bold mb-4 mt-6">Specifications</h3>

                            <dl class="space-y-3 ">
                                <div class="flex items-center gap-3">
                                    <TagIcon/>
                                    <dt class="w-24 font-semibold">Category</dt>
                                    <dd>{{ item.category }}</dd>
                                </div>
                                <div class="flex items-center gap-3">
                                    <PriceIcon/>
                                    <dt class="w-24 font-semibold">Price</dt>
                                    <dd class="font-bold text-lg">{{ item.price }} USD</dd>
                                </div>

                                <div class="pt-4 mt-8 border-t border-neutral-300 text-sm  space-y-1">
                                    <p class="text-right">Updated: <time>{{ new Date(item.updated_at).toLocaleDateString() }}</time></p>
                                </div>
                            </dl>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>