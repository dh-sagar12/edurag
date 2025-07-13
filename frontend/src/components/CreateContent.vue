<template>
    <div class="upload-container">
        <h2>Upload Content</h2>
        <form @submit.prevent="handleSubmit" class="upload-form">
            <div class="form-group">
                <label for="title">Title</label>
                <input type="text" id="title" v-model="form.title" required />
            </div>

            <div class="form-group">
                <label for="topic">Topic</label>
                <input type="text" id="topic" v-model="form.topic" required />
            </div>

            <div class="form-group">
                <label for="grade">Grade</label>
                <input type="text" id="grade" v-model="form.grade" required />
            </div>

            <div class="form-group">
                <label for="file">File</label>
                <input type="file" id="file" @change="handleFileChange" required />
            </div>

            <button type="submit" :disabled="isUploading">{{ isUploading ? 'Uploading...' : 'Upload' }}</button>
        </form>

        <p v-if="message" class="message">{{ message }}</p>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { API_URL } from '../config'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = ref({
    title: '',
    topic: '',
    grade: '',
    file: null ,
})

const message = ref('')
const isUploading = ref(false)

const handleFileChange = (e) => {
    form.value.file = e.target.files[0]
}

const handleSubmit = async () => {
    try {
        const formData = new FormData()
        formData.append('title', form.value.title)
        formData.append('topic', form.value.topic)
        formData.append('grade', form.value.grade)
        if (form.value.file) {
            formData.append('file', form.value.file)
        }

        isUploading.value = true
        const response = await axios.post(`${API_URL}/api/v1/upload-content`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })

        message.value = 'Upload successful: ' + response.data.message
        // Clear form
        form.value = { title: '', topic: '', grade: '', file: null }
        router.push('/content')
    } catch (error) {
        console.error(error)
        message.value = 'Upload failed. Please try again.'
    } finally {
        isUploading.value = false
    }
}
</script>

<style scoped>
.upload-container {
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
}

.form-group {
    margin-bottom: 15px;
}

label {
    font-weight: bold;
}

input[type="text"],
input[type="file"] {
    padding: 8px;
    width: 100%;
    box-sizing: border-box;
}

button {
    padding: 10px;
    background-color: #2563eb;
    color: white;
    border: none;
    cursor: pointer;
}

button:hover {
    background-color: #1e40af;
}

.message {
    margin-top: 15px;
    font-weight: bold;
}
</style>