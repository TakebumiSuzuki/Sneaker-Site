<script setup>
    import apiClient from '@/api'
    import { useSneakerForm } from '@/composables/useSneakerForm'
    import { useRouter } from 'vue-router'

    import AdminBgWrapper from '@/components/AdminBgWrapper.vue';
    import AddImage from '@/components/icons/AddImage.vue';
    import Upload from '@/components/icons/Upload.vue';
    import Loading from '@/components/icons/Loading.vue';
    import AdminGoBack from '@/components/AdminGoBack.vue';

    const router = useRouter()

    const initialFieldData = () => ({
        name: '',
        description: '',
        category: 'running',
        price: null,
        stock: null,
        featured: false,
        image: null,
        delete_image: false
    });

    const initialErrors = ()=>({
        name: null,
        description: null,
        category: null,
        price: null,
        stock: null,
        featured: null,
        image: null,
        serverError: null
    })

    const {
        authStore,
        notificationStore,
        isLoading,
        fieldData,
        resetFieldData,
        errors,
        resetErrors,
        imageURL,
        onFileChange,
        validateFields,
    } = useSneakerForm(initialFieldData, initialErrors)

    const handleSubmit = async () => {
        try {
            resetErrors();
            const formData = new FormData();

            // --- 必須項目 ---
            formData.append('name', fieldData.value.name);
            formData.append('category', fieldData.value.category);

            // --- オプショナル項目（文字列） ---
            // descriptionはnullなら空文字に変換
            formData.append('description', fieldData.value.description || '');

            // --- price (Decimal | None) ---
            // 値が null, undefined, 空文字でない場合にのみ追加。それ以外の場合はそもそもfiledDataに含めない。
            if (fieldData.value.price !== null &&
                typeof fieldData.value.price !== 'undefined' &&
                fieldData.value.price !== ''
            ) {
                formData.append('price', fieldData.value.price);
            }

            // --- stock (int | None) ---
            // 値が null, undefined, 空文字でない場合にのみ追加
            if (fieldData.value.stock !== null &&
                typeof fieldData.value.stock !== 'undefined' &&
                fieldData.value.stock !== ''
            ) {
                formData.append('stock', fieldData.value.stock);
            }

            // --- featured (bool) ---
            // 万が一、何らかの理由で fieldData.value.featured の値が undefined や null になってしまった場合でも、
            // Boolean(undefined) や Boolean(null) は false を返すため、予期せぬエラーを防ぎ、意図通り「チェックされていない」状態として扱われます。
            formData.append('featured', String(Boolean(fieldData.value.featured)));
            // ★ポイント2: これにより、fieldData.value.featuredが `undefined` や `null` の場合は 'false' という文字列が送信されます。
            // Pydanticは 'true' や 'false' という文字列を正しくbool値に解釈できるため、エラーを防げます。

            // --- 画像ファイル ---
            if (fieldData.value.image) {
                formData.append('image', fieldData.value.image);
            }

            validateFields();

            if (Object.values(errors.value).some(err => err !== null)) { return;}

            isLoading.value = true;
            await apiClient.post('/api/sneakers/', formData);

            resetFieldData();
            notificationStore.showNotification('スニーカーを登録しました！', 'success'); // メッセージを状況に合わせて変更
            router.push({name: 'admin-items'})

        } catch (err) {
            console.error('API request failed:', err);
            errors.value.serverError = err.response?.data?.detail || '登録に失敗しました。入力内容を確認してください。'; // FastAPI/Pydanticのエラーはdetailに入ることが多い
            notificationStore.showNotification('登録に失敗しました。', 'error');

        } finally {
            isLoading.value = false;
        }
    };

</script>


<template>
    <AdminBgWrapper>
        <div class="px-2 md:px-6 py-2">
            <div class="max-w-[900px] mx-auto w-full">
                    <AdminGoBack class=""/>
            </div>
            <div class="justify-center max-w-[600px] w-full mx-auto">

                <div class="text-4xl tracking-wide pb-6 pt-10 text-center">
                    Add Item
                </div>

                <form @submit.prevent="handleSubmit" novalidate class="px-4 md:px-8 w-full">
                    <p v-if="errors.serverError" class="text-red-500 text-sm mb-1">{{ errors.serverError }}</p>

                    <div>
                        <p v-if="errors.name" class="text-red-500 text-sm mb-1">{{ errors.name }}</p>
                        <label for="name-field" class="block">Item Name:</label>
                        <input type="text" id="name-field" v-model.trim="fieldData.name"
                            class="border px-4 py-2 rounded w-full mb-6 shadow-sm"
                        >
                    </div>

                    <div>
                        <p v-if="errors.description"  class="text-red-500 text-sm mb-1">{{ errors.description }}</p>
                        <label for="description-field" class="block">Description:</label>
                        <textarea
                            name="description" id="description-field" rows="10"
                            v-model.trim="fieldData.description"
                            class="border px-4 py-2 rounded w-full mb-6 shadow-sm"
                        ></textarea>
                    </div>

                    <div>
                        <p v-if="errors.category"  class="text-red-500 text-sm mb-1">{{ errors.category }}</p>
                        <label for="category-field" class="block">Category:</label>
                        <select id="category-field" v-model="fieldData.category"
                            class="border px-4 py-1.5 rounded mb-6 shadow-sm"
                        >
                            <option value="running">Running</option>
                            <option value="basketball">Basketball</option>
                            <option value="lifestyle">Lifestyle</option>
                            <option value="training">Training</option>
                        </select>
                    </div>

                    <div>
                        <p v-if="errors.price"  class="text-red-500 text-sm mb-1">{{ errors.price }}</p>
                        <label for="price-field" class="block">Price:</label>
                        <input type="number" id="price-field" v-model.number="fieldData.price"
                            step="0.01" min="0"
                            class="border px-4 py-2 rounded mb-6 shadow-sm"
                        >
                    </div>

                    <div>
                        <p v-if="errors.stock"  class="text-red-500 text-sm mb-1">{{ errors.stock }}</p>
                        <label for="stock-field" class="block">Stock:</label>
                        <input type="number" id="stock-field"  v-model.number="fieldData.stock"
                            step="1"
                            class="border px-4 py-2 rounded mb-6 shadow-sm"
                        >
                    </div>

                    <div>
                        <p v-if="errors.featured"  class="text-red-500 text-sm mb-1">{{ errors.featured }}</p>
                        <label for="featured-field" class="mr-2">Featured:</label>
                        <input type="checkbox" id="featured-field" v-model="fieldData.featured"
                            class="size-4 mb-6"
                        >
                    </div>

                    <div>
                        <p v-if="errors.image" class="text-red-500 text-sm mb-1">{{ errors.image }}</p>
                        <label for="image-field"
                            class="block cursor-pointer rounded-md bg-neutral-400 px-6 py-2 text-sm font-semibold text-white shadow-sm hover:bg-neutral-500 active:bg-neutral-600 transition size-fit ease-in-out">
                            <div class="flex items-center gap-1">
                            <AddImage class="size-4.5"></AddImage>Add Image
                            </div>
                        </label>

                        <!-- 実際のファイル入力。ユーザーからは見えないようにする -->
                        <input type="file" id="image-field" class="hidden" accept="image/*"
                            @change="onFileChange"
                        >
                    </div>

                    <div v-if="imageURL">
                        <img :src="imageURL" alt="selected picture" class="w-full max-w-[400px] max-h-[400px] object-contain block mx-auto mt-4">
                    </div>

                    <button
                        type="submit"
                        class="px-4 py-2 w-full text-white font-semibold mb-6 mt-10 rounded-md shadow-sm
                        cursor-pointer bg-gradient-to-br from-indigo-400 to-indigo-500 opacity-80
                        hover:opacity-90 active:opacity-100 transition ease-in-out"
                        :disabled="isLoading"
                    >
                        <div v-if="isLoading" class="flex items-center justify-center gap-2">
                            <Loading class="animate-spin size-5"></Loading>
                            Processing...
                        </div>
                        <div v-else class="flex items-center justify-center gap-2">
                            <Upload class="size-5"></Upload>Submit
                        </div>
                    </button>
                </form>

            </div>
        </div>


    </AdminBgWrapper>

</template>