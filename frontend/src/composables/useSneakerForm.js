import { onMounted, ref, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notification';

export function useSneakerForm(initialFieldData, initialErrors) {

    const authStore = useAuthStore()
    const notificationStore = useNotificationStore();
    const isLoading = ref(false)

    const fieldData = ref(initialFieldData());
    const errors = ref(initialErrors());
    const imageURL = ref(null)
    const deleteImage = ref(false); // Edit Itemでのみ使う


    function resetFieldData() {
        fieldData.value = initialFieldData();
        if (imageURL.value) {
            URL.revokeObjectURL(imageURL.value);
            imageURL.value = null;
        }
    }

    function resetErrors(){
        errors.value = initialErrors();
    }


    function onFileChange(event) {
        const files = event.target.files;

        // 以前のプレビューURLがもしあれば、ここで解放する
        if (imageURL.value) {
            URL.revokeObjectURL(imageURL.value);
        }
        if (files.length) {
            fieldData.value.image = files[0];  // 単一ファイル
            imageURL.value = URL.createObjectURL(files[0])
        }else{
            fieldData.value.image = null;
            imageURL.value = null
        }
    }


    function validateFields(){
        if (!fieldData.value.name){
            errors.value.name = 'You must enter item name.'
        }else if (fieldData.value.name.length > 50){
            errors.value.name = 'Item name is too long.'
        }

        if (fieldData.value.description && fieldData.value.description.length > 1000){
            errors.value.description = 'Description is too long.'
        }

        if (!fieldData.value.category){
            errors.value.category = 'You must enter category.'
        }else if (!['running', 'basketball', 'training', 'lifestyle'].includes(fieldData.value.category)){
            errors.value.category = 'Choose the correct category.'
        }

        const price = fieldData.value.price;
        // priceが未入力(null, undefined, 空文字)でない場合にバリデーションを実行
        if (price !== null && typeof price !== 'undefined' && price !== '') {

            if (price < 0) {
                errors.value.price = '価格にマイナスの値は設定できません。';
            } else {
                const priceStr = String(price);
                if (priceStr.includes('.') && priceStr.split('.')[1].length > 2) {
                    errors.value.price = '価格は小数点第2位まで入力できます。';
                } else if (priceStr.split('.')[0].length > 8) {
                    errors.value.price = '価格の整数部分が大きすぎます（最大8桁）。';
                }
            }
        }

        const stock = fieldData.value.stock;
        // stockが未入力(nullや空文字)でない場合にバリデーションを実行
        if (stock !== null && stock !== '') {
            // まず、値が「整数」であるかをチェックする
            if (!Number.isInteger(stock)) {
                errors.value.stock = '在庫数には有効な整数を入力してください。';
            }
            // 整数であることが確認できた上で、範囲のチェックを行う
            else if (stock < 0 || stock > 10000) {
                errors.value.stock = '在庫数は0以上、10000以下で入力してください。';
            }
        }

        if (fieldData.value.image) {
            const imageFile = fieldData.value.image;
            const maxSizeInBytes = 15 * 1024 * 1024;

            if (imageFile.size > maxSizeInBytes) {
                errors.value.image = 'File is too large. Please upload an image under 15MB.';
            } else if (!['image/jpeg', 'image/png', 'image/gif', 'image/webp'].includes(imageFile.type)) {
                errors.value.image = 'Invalid file type. Please upload a JPEG, PNG, GIF, or WebP image.';
            }
        }
    }

    onMounted(async()=>{
        console.log('3秒後にユーザーデータを表示します...')
        // 3秒間待機する
        await new Promise(resolve => setTimeout(resolve, 3000))
        // 3秒後に実行される
        console.log(`ユーザーのデータ`, authStore.user)
        console.log(`最初のデーター:`, fieldData.value)
    })

    onUnmounted(() => {
        if (imageURL.value) {
            URL.revokeObjectURL(imageURL.value);
        }
    });

    function deleteImagePressed(){
        console.log('deleteImagePress was pressed')
        deleteImage.value = true
        if (imageURL.value) {
            URL.revokeObjectURL(imageURL.value); // 先にURLを解放する
        }
        imageURL.value = null; // その後にnullを設定する
    }


    return {
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
    }
}