<template>
    <div class="metrix-container">
      <h2>Dashboard Metrics</h2>
  
      <div v-if="loading" class="loading">Loading...</div>
      <div v-if="error" class="error">{{ error }}</div>
  
      <div class="metrix-grid" v-if="!loading && !error">
        <div class="metrix-card">
          <h3>Total Topics</h3>
          <p>{{ metrix.total_topics }}</p>
        </div>
  
        <div class="metrix-card">
          <h3>Total Files Uploaded</h3>
          <p>{{ metrix.total_file_uploaded }}</p>
        </div>
  
        <div class="metrix-card">
          <h3>Total Queries</h3>
          <p>{{ metrix.total_queries }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  import { API_URL } from '../config'
  
  const metrix = ref({
    total_topics: 0,
    total_file_uploaded: 0,
    total_queries: 0
  })
  
  const loading = ref(false)
  const error = ref('')
  
  const fetchMetrix = async () => {
    loading.value = true
    try {
      const response = await axios.get(`${API_URL}/api/v1/metrix`)
      metrix.value = response.data
    } catch (err) {
      console.error(err)
      error.value = 'Failed to load metrics.'
    } finally {
      loading.value = false
    }
  }
  
  onMounted(() => {
    fetchMetrix()
  })
  </script>
  
  <style scoped>
  .metrix-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    font-family: sans-serif;
  }
  
  h2 {
    text-align: center;
    margin-bottom: 30px;
    font-size: 28px;
  }
  
  .metrix-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
  }
  
  .metrix-card {
    background: linear-gradient(135deg, #2563eb, #1e40af);
    color: white;
    padding: 30px 20px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    text-align: center;
    transition: transform 0.2s ease;
  }
  
  .metrix-card:hover {
    transform: translateY(-5px);
  }
  
  .metrix-card h3 {
    margin-bottom: 10px;
    font-size: 20px;
  }
  
  .metrix-card p {
    font-size: 32px;
    font-weight: bold;
  }
  
  .loading, .error {
    text-align: center;
    font-size: 18px;
    margin-top: 20px;
  }
  
  .error {
    color: red;
  }
  </style>
  