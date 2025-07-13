<template>
    <div class="content-container">
        <h2>Content List</h2>

        <!-- Filters -->
        <div class="filters">
            <input type="text" v-model="filters.grade" placeholder="Filter by grade" />
            <input type="text" v-model="filters.title" placeholder="Filter by title" />
            <button @click="applyFilters">Apply Filters</button>
            <button @click="resetFilters">Reset</button>
            <button @click="goToCreateContent">Create Content</button>
        </div>


        <!-- Content Table -->
        <table>
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Topic</th>
                    <th>Grade</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in content" :key="item.title + item.grade + item.topic">
                    <td>{{ item.title }}</td>
                    <td>{{ item.topic }}</td>
                    <td>{{ item.grade }}</td>
                    <td>
                        <button @click="goToAsk(item)">Ask</button>
                    </td>
                </tr>
            </tbody>
        </table>

        <p v-if="loading">Loading...</p>
        <p v-if="error" class="error">{{ error }}</p>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { API_URL } from '../../config'

const router = useRouter()
const content = ref([])
const loading = ref(false)
const error = ref('')
const filters = ref({
    grade: '',
    title: '',
})

const fetchContent = async (grade = '', title = '') => {
    loading.value = true
    try {
        const params = {}
        if (grade) params.grade = grade
        if (title) params.title = title

        const response = await axios.get(`${API_URL}/api/v1/topics`, { params })
        content.value = response.data
    } catch (err) {
        console.error(err)
        error.value = 'Failed to load content.'
    } finally {
        loading.value = false
    }
}

const applyFilters = () => {
    fetchContent(filters.value.grade, filters.value.title)
}

const resetFilters = () => {
    filters.value.grade = ''
    filters.value.title = ''
    fetchContent()
}

const goToAsk = (item) => {
    router.push('/ask?context_id=' + item.id)
}

const goToCreateContent = () => {
    router.push('/content/create')
}

onMounted(() => {
    fetchContent()
})
</script>

<style scoped>
.content-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.filters {
    margin-bottom: 20px;
}

.filters input {
    padding: 8px;
    margin-right: 10px;
}

.filters button {
    padding: 8px 12px;
    margin-right: 5px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
}

th,
td {
    border: 1px solid #ccc;
    padding: 10px;
    text-align: left;
}

th {
    background-color: #f0f0f0;
}


button:hover {
    background-color: #1e40af;
}

.error {
    color: red;
    margin-top: 10px;
}
</style>