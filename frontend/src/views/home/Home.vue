<script setup>
    import { ref, watch, onBeforeUnmount } from 'vue'
    import apiClient from '@/api'

    import CategoryLabel from '@/components/CategoryLabel.vue';
    import Pagination from '@/components/Pagination.vue'
    import Loading from '@/components/icons/Loading.vue'

    const items = ref([])
    const meta = ref(null); // ページネーション情報を格納
    const isLoading = ref(false);
    const page = ref(1)
    const perPage = 6
    const query = ref('')
    const error = ref(null)

    const fetchItems = async() => {
        isLoading.value = true;
        error.value = null
        try {
            const response = await apiClient.get(`/api/sneakers`, {
                params: {
                    q: query.value.trim(),
                    page: page.value,
                    per_page: perPage
                }
            });
            // APIからのレスポンス構造に合わせてデータを格納
            items.value = response.data.items;
            meta.value = response.data.meta;
            console.log("Fetched data:", response.data);

        } catch (err) {
            console.error("Failed to fetch items:", err.response?.data?.message || err.message);
            // エラー発生時にリストを空にするなどの対応
            items.value = [];
            meta.value = null;
            error.value = 'An error occurred. Please try again later.'
        } finally {
            isLoading.value = false;
        }
    };


    let timer = null

    watch([page, query], (newValue, oldValue)=> {
        let delay = 0
        if (newValue[1] !== oldValue[1]){
            // queryが1文字の時は一切処理しない。0文字になった時にはqueryを使わない全部ヒットの検索になる。
            if (query.value.length === 1){
                return
            }
            delay = 300
            page.value = 1
        }
        if (timer){
            clearTimeout(timer)
        }
        timer = setTimeout(()=>{
            fetchItems()
        }, delay)
    }, { immediate: true })

    onBeforeUnmount(() => {
        if (timer) clearTimeout(timer)
    })

    // Paginationコンポーネントから送られてきたイベントが最終的にここで処理される
    const handlePageChange = (newPage) => {
        if (newPage >= 1 && newPage <= meta.value.total_pages && newPage !== page.value) {
            page.value = newPage
        }
    };
</script>



<template>
    <div class="px-4 md:px-8 pb-16 bg-gradient-to-br from-neutral-500 to-neutral-600">
        <div class="w-full max-w-[1200px] mx-auto text-neutral-50">

            <div>
                <input
                    type="search"
                    placeholder="search..."
                    v-model.trim="query"
                    class="px-4 py-1.5 border rounded-md border-neutral-400 block mx-auto mt-6 md:mt-10 outline-none focus:bg-neutral-50/20 focus:border-neutral-200 w-full max-w-[350px] shadow-sm"
                >
            </div>

            <div v-if="isLoading" class="mt-16 p-4 text-sky-400/50 ">
                <Loading class="animate-spin mx-auto size-14" />
            </div>

            <div v-else="error" class="text-center mt-6 p-4 bg-red-500/20 text-red-200 rounded-md">
                {{ error }}
            </div>

            <div v-else>
                <div class="mt-6 grid grid-cols-1 gap-8 md:mt-10 md:grid-cols-3 md:gap-10 mx-auto ">
                    <div v-for="item in items" :key="item.id">
                        <RouterLink :to="{name: 'product-detail', params: {id: item.id}}" >
                            <div class="hover:scale-103 hover:opacity-80 transition ease-in-out">
                            <div class="relative rounded-md overflow-clip shadow-sm">
                                <img :src="item.image_url" :alt="item.name" class="block w-full shadow-md ">
                                <CategoryLabel :label="item.category"></CategoryLabel>
                            </div>
                            <div class="flex justify-between items-center">
                                <p class="text-sm">{{ item.name }}<span v-if="item.featured" class="text-xs bg-orange-400 text-white px-1 rounded ml-1 opacity-80">Hot</span></p>
                                <p class="text-sm">${{ item.price }}</p>
                            </div>
                            </div>
                        </RouterLink>
                    </div>
                </div>

                <Pagination
                    v-if="meta && meta.total_pages > 1"
                    :meta="meta"
                    @change-page="handlePageChange">
                </Pagination>
            </div>

        </div>

    </div>

</template>