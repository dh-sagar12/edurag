<template>
    <div class="dashboard-container">
        <!-- Sidebar -->
        <div class="sidebar">
            <div class="sidebar-header">AI Tutor</div>
            <nav class="sidebar-menu">
                <ul>
                    <router-link to="/home" class="router-link">
                        <li>Home</li>
                    </router-link>
                    <router-link to="/ask" class="router-link">
                        <li>Ask</li>
                    </router-link>
                    <router-link to="/content" class="router-link">
                        <li>Content</li>
                    </router-link>
                </ul>
            </nav>
        </div>

        <!-- Main Content Area -->
        <div class="main-content">
            <router-view />
        </div>
    </div>
</template>

<script setup lang="ts">


</script>

<style scoped>
.dashboard-container {
    display: flex;
    height: 100vh;
    background-color: #f3f4f6;
    font-family: sans-serif;
}

.sidebar {
    width: 250px;
    background-color: #fff;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.sidebar-header {
    padding: 20px;
    font-size: 24px;
    font-weight: bold;
    border-bottom: 1px solid #ddd;
}

.sidebar-menu ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.sidebar-menu li {
    padding: 15px 20px;
    border-bottom: 1px solid #eee;
}

.router-link {
    text-decoration: none;
    color: #333;
    list-style: none;
}

.sidebar-menu li:hover {
    background-color: #f0f0f0;
}

.main-content {
    flex: 1;
    padding: 30px;
}
</style>