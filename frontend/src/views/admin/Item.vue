
<script setup>
    import { onMounted, ref, computed } from 'vue';
    import { useRouter } from 'vue-router'
    import { useNotificationStore } from '@/stores/notification'
    import { useAlertStore } from '@/stores/alert';

    import apiClient from '@/api'
    import AdminBgWrapper from '@/components/AdminBgWrapper.vue'
    import TagIcon from '@/components/icons/TagIcon.vue'
    import PriceIcon from '@/components/icons/PriceIcon.vue'
    import StockIcon from '@/components/icons/StockIcon.vue'
    import FeaturedIcon from '@/components/icons/FeaturedIcon.vue'
    import Loading from '@/components/icons/Loading.vue'
    import Update from '@/components/icons/Update.vue'
    import Delete from '@/components/icons/Delete.vue'
    import AdminGoBack from '@/components/AdminGoBack.vue';

    const router = useRouter()
    const notification = useNotificationStore()
    const alert = useAlertStore()

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

    const handleDelete = async ()=>{
        try{
            const result = await alert.showAlert(
                'Are you sure you want to delete this item?',
                [{ text: 'Yes', value: true, style: 'primary' }, { text: 'Cancel', value: false, style: 'secondary' }]
            )
            if (result){
                await apiClient.delete(`/api/sneakers/${numericId.value}`)
                notification.showNotification('Item successfully deleted', 'success')
                router.push({ name: 'admin-items' })
            }

        }catch(err){
            console.log('Failed to delete item')
            notification.showNotification('Failed to delete item. Please try it later again.', 'error')
        }
    }
</script>


<template>
    <AdminBgWrapper>
        <div class="px-2 md:px-8 py-2">
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

                <div class="flex items-center justify-center gap-6 size-fit ml-auto mb-6">
                    <RouterLink :to="{ name: 'admin-item-edit', params: { id: numericId }} ">
                        <div class="border px-6 py-2 rounded-lg text-white bg-indigo-400 hover:cursor-pointer hover:bg-indigo-500 transition active:bg-indigo-600 font-semibold shadow-sm flex items-center gap-2">
                            <Update class="size-4.5"></Update>
                            Edit
                        </div>
                    </RouterLink>
                    <div
                        @click="handleDelete"
                        class="border px-6 py-2 rounded-lg text-white bg-pink-400 hover:cursor-pointer hover:bg-pink-500 transition active:bg-pink-600 font-semibold shadow-sm mr-6 flex items-center gap-2">
                        <Delete class="size-4.5"></Delete>
                        Delete
                    </div>

                </div>

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
                            <h3 class="text-xl font-bold text-neutral-800 mb-2">Description</h3>
                            <p class="text-neutral-700 leading-relaxed">{{ item.description }}</p>
                        </div>

                        <!-- Specifications -->
                        <div>
                            <h3 class="text-xl font-bold text-neutral-800 mb-4 mt-6">Specifications</h3>

                            <dl class="space-y-3 text-neutral-700">
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
                                <div class="flex items-center gap-3">
                                    <StockIcon/>
                                    <dt class="w-24 font-semibold">Stock</dt>
                                    <dd>{{ item.stock }}</dd>
                                </div>
                                <div class="flex items-center gap-3">
                                    <FeaturedIcon/>
                                    <dt class="w-24 font-semibold">Featured</dt>
                                    <dd>{{ item.featured ? 'Yes' : 'No' }}</dd>
                                </div>

                                <div class="pt-4 mt-8 border-t border-neutral-300 text-sm text-neutral-400 space-y-1">
                                    <p class="text-right">Created: <time>{{ new Date(item.created_at).toLocaleDateString() }}</time></p>
                                    <p class="text-right">Updated: <time>{{ new Date(item.updated_at).toLocaleDateString() }}</time></p>
                                </div>
                            </dl>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </AdminBgWrapper>
</template>