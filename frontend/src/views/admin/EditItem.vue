
<script setup>
    import AdminBgWrapper from '@/components/AdminBgWrapper.vue';
    import { useSneakerForm } from '@/composables/useSneakerForm'
    import { onMounted } from 'vue'
    import apiClient from '@/api'
    import { useRouter } from 'vue-router'
    import AdminGoBack from '@/components/AdminGoBack.vue';


    const router = useRouter()
    const props = defineProps({ id: String });

    const initialFieldData = () => ({
        name: null,
        description: null,
        category: 'running',
        price: null,
        stock: null,
        featured: false,
        image: null
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
        deleteImage,
        deleteImagePressed
        } = useSneakerForm(initialFieldData, initialErrors)


    let initialLocalData = null

    onMounted(async()=>{
        try{
            const response = await apiClient.get(`/api/sneakers/${props.id}`)
            const initialData = response.data

            initialLocalData = { ...initialData }
            // submitの際にこのinitialLocalDataのimageURLと、ユーザーが再度選択したimageURLを比べる。
            initialLocalData.imageURL = initialData.image_url
            fieldData.value = { ...initialData, imageURL: initialData.image_url }
            imageURL.value = initialData.image_url

        }catch(err){
            console.log('エラーです', err)
        }
    })

    const handleSubmit = async () => {
        try {
            resetErrors();

            const formData = new FormData();

            // --- 必須項目 ---
            if (initialLocalData.name !== fieldData.value.name){
                formData.append('name', fieldData.value.name);
            }

            if (initialLocalData.category !== fieldData.value.category){
                formData.append('category', fieldData.value.category);
            }

            // --- オプショナル項目（文字列） ---
            // descriptionはnullなら空文字に変換
            if (initialLocalData.description !== fieldData.value.description){
                formData.append('description', fieldData.value.description || '');
            }

            // --- 画像ファイル ---
            if (fieldData.value.image && initialLocalData.image_url !== imageURL) {
                formData.append('image', fieldData.value.image);
            }
            if (deleteImage.value){
                formData.append('delete_image', 'true')
            }else{
                formData.append('delete_image', 'false')
            }

            // --- price (Decimal | None) ---
            // 値が null, undefined, 空文字でない場合にのみ追加
            if (initialLocalData.price !== fieldData.value.price &&
                fieldData.value.price !== null &&
                typeof fieldData.value.price !== 'undefined' &&
                fieldData.value.price !== ''
            ) {
                formData.append('price', fieldData.value.price);
            }

            // --- stock (int | None) ---
            // 値が null, undefined, 空文字でない場合にのみ追加
            if (initialLocalData.stock !== fieldData.value.stock &&
                fieldData.value.stock !== null &&
                typeof fieldData.value.stock !== 'undefined' &&
                fieldData.value.stock !== ''
            ) {
                formData.append('stock', fieldData.value.stock);
            }
            // ★ポイント1: stockに値がない場合、formDataにキーが追加されません。
            // これにより、バックエンドのPydanticモデルはデフォルト値の `None` を使用します。

            // --- featured (bool) ---
            // Boolean()で値を確実にtrue/falseに変換し、String()で文字列化して追加
            if (initialLocalData.featured !== fieldData.value.featured){
                formData.append('featured', String(Boolean(fieldData.value.featured)));
            }


            // ★ポイント2: これにより、fieldData.value.featuredが `undefined` や `null` の場合は 'false' という文字列が送信されます。
            // Pydanticは 'true' や 'false' という文字列を正しくbool値に解釈できるため、エラーを防げます。

            validateFields();

            if (Object.values(errors.value).some(err => err !== null)) {
                return;
            }
            isLoading.value = true;
            console.log('---送られるデータ----')
            formData.forEach((value, key) => console.log(key, value));
            await apiClient.patch(`/api/sneakers/${props.id}`, formData);
            notificationStore.showNotification('The item information was updated successfully.', 'success'); // メッセージを状況に合わせて変更
            router.push({name: 'admin-item-detail', params: { id: props.id}})

        } catch (err) {
            console.error('API request failed:', err);
            errors.value.serverError = err.response?.data?.detail || '更新に失敗しました。入力内容を確認してください。'; // FastAPI/Pydanticのエラーはdetailに入ることが多い
            notificationStore.showNotification('Failed to update the item. Please try again later.', 'error');
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
            <div class=" max-w-[600px] w-full mx-auto ">
                <div class="text-4xl tracking-wide pb-6 pt-10 text-center">
                    Edit Item
                </div>

                <form @submit.prevent="handleSubmit" novalidate class="px-2 md:px-4 w-full">
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
                        <input type="number" id="stock-field"v-model.number="fieldData.stock"
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
                            class="block cursor-pointer rounded-md bg-neutral-400 px-6 py-2 text-sm font-semibold text-white shadow-sm hover:bg-neutral-500 active:bg-neutral-600 transition size-fit">
                            Add Image
                        </label>

                        <!-- 実際のファイル入力。ユーザーからは見えないようにする -->
                        <input type="file" id="image-field" class="hidden" accept="image/*" @change="onFileChange">

                        <div v-if="(imageURL && imageURL === initialLocalData?.image_url)"
                            class="block cursor-pointer rounded-md bg-pink-400 px-6 py-2 text-sm font-semibold text-white shadow-sm hover:bg-pink-500 active:bg-pink-600 transition size-fit mt-4"
                            @click="deleteImagePressed"
                        >
                            Delete Image
                        </div>
                    </div>

                    <div v-if="imageURL">
                        <img :src="imageURL" alt="selected picture" class="w-full max-w-[400px] max-h-[400px] object-contain block mx-auto mt-4">
                    </div>


                    <button type="submit"
                        class="px-4 py-2 w-full text-white font-semibold mb-6 mt-10 rounded-md shadow-sm
                        cursor-pointer bg-gradient-to-br from-indigo-400 to-indigo-500 opacity-80
                        hover:opacity-90 active:opacity-100 transition"
                        :disabled="isLoading"
                    >
                        {{ isLoading ? 'Processing...' : 'Submit' }}
                    </button>
                </form>

            </div>

        </div>
    </AdminBgWrapper>

</template>