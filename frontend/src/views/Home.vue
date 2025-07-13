<template>
    <h1>Home</h1>
    <div v-if="showUpload">
        <p>No Content to ask Please Create Content</p>
        <button @click="goToCreateContent">Create Content</button>
    </div>
    <div v-else>
        <metrix />
        <div class="ask-button-div">
            <button @click="goToAsk" class="btn-large">Ask Your Question</button>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
// @ts-ignore
import axios from 'axios';
// @ts-ignore
import { API_URL } from '../config';
// @ts-ignore
import { useRouter } from 'vue-router';
// @ts-ignore
import Metrix from '../components/Metrix.vue';

const router = useRouter()
const showUpload = ref(true);

onMounted(() => {
    axios.get(`${API_URL}/api/v1/topics`)
        .then((response) => {
            if (response.data && response.data.length > 0) {
                showUpload.value = false;
            }
        })
        .catch((error) => {
            console.error(error);
        });
});

const goToCreateContent = () => {
    router.push('/content/create')
}

const goToAsk = () => {
    router.push('/ask')
}
</script>

<style scoped>
.ask-button-div {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}
</style>
