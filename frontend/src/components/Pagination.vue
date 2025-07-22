<script setup>
    import { computed } from 'vue'
    const props = defineProps({
        // props.metaオブジェクトを受け取る。必須項目とする。
        meta: {
            type: Object,
            required: true
        }
    })

    const emit = defineEmits(['change-page'])
    const onPageClick = (page)=>{
        emit('change-page', page)
    }


    // 表示するページ番号のリストを計算する
    // これにより、ページ数が多くなってもUIが崩れない (例: 1 2 ... 5 6 7 ... 19 20)
    const pagesToShow = computed(() => {
        if (!props.meta) return [];

        const currentPage = props.meta.page;
        const totalPages = props.meta.total_pages;
        const range = 2; // 現在ページの前後に表示するページ数
        const pages = [];

        for (let i = 1; i <= totalPages; i++) {
            if (i === 1 || i === totalPages || (i >= currentPage - range && i <= currentPage + range)) {
                pages.push(i);
            }
        }

        const pagesWithEllipsis = [];
        let lastPage = 0;
        for (const page of pages) {
            if (lastPage) {
                if (page - lastPage === 2) {
                    pagesWithEllipsis.push(lastPage + 1);
                } else if (page - lastPage > 2) {
                    pagesWithEllipsis.push('...');
                }
            }
            pagesWithEllipsis.push(page);
            lastPage = page;
        }

        return pagesWithEllipsis;
    });

</script>

<template>
    <!-- Pagination UI -->
    <div class="flex items-center justify-center space-x-2 mt-8 text-neutral-600">
        <!-- Previous Page Button -->
        <button
            @click="onPageClick(props.meta.page - 1)"
            :disabled="props.meta.page === 1"
            class="px-3 py-1 rounded-md bg-white border border-gray-300 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
        >
            « Prev
        </button>

        <!-- Page Number Buttons -->
        <template v-for="(page, index) in pagesToShow" :key="index">
            <span v-if="page === '...'" class="px-3 py-1 text-gray-500">...</span>
            <button v-else
                @click="onPageClick(page)"
                :class="[
                    'px-3 py-1 rounded-md border',
                    page === props.meta.page
                        ? 'bg-indigo-300 text-white border-indigo-600'
                        : 'bg-white border-gray-300 hover:bg-gray-100'
                ]"
            >
                {{ page }}
            </button>
        </template>

        <!-- Next Page Button -->
        <button
            @click="onPageClick(props.meta.page + 1)"
            :disabled="props.meta.page === props.meta.total_pages"
            class="px-3 py-1 rounded-md bg-white border border-gray-300 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
        >
            Next »
        </button>
    </div>

</template>