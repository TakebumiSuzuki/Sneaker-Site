
<script setup>
    import { ref, watch, onUnmounted } from 'vue';
    import apiClient from '@/api';

    import AdminBgWrapper from '@/components/AdminBgWrapper.vue';
    import Loading from '@/components/icons/Loading.vue'
    import Add from '@/components/icons/Add.vue'
    import Pagination from '@/components/Pagination.vue';

    const items = ref([]); // itemsは空の配列で初期化するのが一般的
    const meta = ref(null); // ページネーション情報を格納
    const isLoading = ref(false);
    const page = ref(1)
    const perPage = 5
    const query = ref('')
    const error = ref(null)


    const fetchItems = async() => {
        isLoading.value = true;
        error.value = null
        try {
            const response = await apiClient.get(`/api/sneakers/`, {
                params: {
                    page: page.value,
                    per_page: perPage,
                    q: query.value
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
            error.value = 'Failed to fetch data. Please tray again later.'
        } finally {
            isLoading.value = false;
        }
    };

    let timer = null
    watch([page, query], (newValue, oldValue)=>{
        let delay = 0
        if (newValue[1] !== oldValue[1]){
            if (newValue[1].length === 1){
                return
            }
            page.value = 1
            delay = 300
        }
        if (timer){ clearTimeout() }
        timer = setTimeout(()=>{
            fetchItems()
        }, delay)
    }, { immediate: true })

    onUnmounted(()=>{
        if (timer){ clearTimeout() }
    })

    // --- ページネーションのページボタンがクリックされたらデータを読み込む ---
    const changePage = (newPage) => {
        if (newPage >= 1 && newPage <= meta.value.total_pages && newPage !== meta.value.page) {
            page.value = newPage;
        }
    };


</script>

<template>
    <AdminBgWrapper>
        <div class="px-2 md:px-6">
            <div class="py-12 max-w-[900px] w-full mx-auto">
                <div class="text-4xl tracking-wide pb-10 text-center">
                    Items
                </div>

                <div class="flex justify-between items-center mb-6">
                    <input type="search" placeholder="Search..." v-model="query"
                        class="border border-neutral-300 px-4 py-1.5 rounded-md outline-none focus:border-neutral-400 w-[300px]"
                    >

                    <RouterLink :to="{name: 'admin-item-create'}" >
                        <div class="font-semibold size-fit ml-auto px-4 py-2 rounded-md text-white bg-indigo-400 hover:bg-indigo-500 active:bg-indigo-600 shadow-sm transition flex items-center gap-2">
                            <Add class="size-5"></Add>
                            Add Item
                        </div>
                    </RouterLink>
                </div>

                <div v-if="isLoading" class="">
                    <Loading class="animate-spin text-sky-500/30 size-14 mx-auto mt-16"></Loading>
                </div>

                <div v-else-if="error">{{ error }}</div>

                <div v-else-if="items && items.length > 0">

                    <!-- ヘッダー -->
                    <div class="hidden md:grid md:grid-cols-[30px_50px_1fr_100px_80px_100px_80px] md:gap-4 p-2 border-b-2 font-bold">
                        <p class="text-center">ID</p>
                        <p></p>
                        <p>Name</p>
                        <p class="text-center">Category</p>
                        <p class="text-right pr-6">Stock</p>
                        <p class="text-right pr-6">Price</p>
                        <p class="text-center">Featured</p>
                    </div>

                    <!-- アイテムリスト -->
                    <div v-for="item in items" :key="item.id">
                        <RouterLink :to="{name:'admin-item-detail', params: {id: item.id}}">
                            <div class="p-2 md:p-0 border-b border-neutral-200 hover:bg-neutral-100 transition cursor-pointer">
                                <div class="md:hidden flex items-center space-x-4 p-2">
                                    <img :src="item.image_url" alt="" class="h-16 w-16 object-cover rounded-md">
                                    <div class="flex-grow">
                                        <p class="font-semibold">{{ item.name }}</p>
                                        <p class="text-sm text-gray-600">{{ item.category }}</p>
                                    </div>
                                    <div class="text-right">
                                        <p class="font-semibold">{{ item.price }} USD</p>
                                        <p class="text-sm text-gray-500">stock: {{ item.stock }}</p>
                                    </div>
                                </div>
                                <div class="hidden md:grid md:grid-cols-[30px_50px_1fr_100px_80px_100px_80px] md:gap-4 items-center h-16 p-2">
                                    <p class="text-center">{{ item.id }}</p>
                                    <img :src="item.image_url" alt="" class="h-12 block mx-auto">
                                    <p>{{ item.name }}</p>
                                    <p class="text-center">{{ item.category }}</p>
                                    <p class="text-right pr-6">{{ item.stock }}</p>
                                    <p class="text-right pr-6">{{ item.price }}</p>
                                    <p class="text-center">{{ item.featured }}</p>
                                </div>
                            </div>
                        </RouterLink>
                    </div>

                    <div v-if="meta && meta.total_pages > 1">
                        <Pagination :meta="meta" @change-page="changePage"></Pagination>
                    </div>
                </div>



            </div>
        </div>
    </AdminBgWrapper>
</template>