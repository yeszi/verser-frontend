<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 to-indigo-900">
    <div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-md">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800">VeriZh Chain</h1>
        <p class="text-gray-600 mt-2">Digital Certificate Verification System</p>
      </div>
      
      <div v-if="error" class="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
        {{ error }}
      </div>
      
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2">Username</label>
          <input 
            v-model="username" 
            type="text" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Masukkan username"
            required
          />
        </div>
        
        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2">Password</label>
          <input 
            v-model="password" 
            type="password" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Masukkan password"
            required
          />
        </div>
        
        <button 
          type="submit" 
          :disabled="loading"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md disabled:opacity-50"
        >
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
      
      <button 
        @click="testConnection" 
        class="w-full mt-4 text-sm text-gray-500 hover:text-gray-700"
      >
        Test Connection
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import API_BASE_URL from '../config/api'

export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: '',
      loading: false,
      error: null
    }
  },
  methods: {
    async testConnection() {
      try {
        this.error = null
        const res = await axios.get(`${API_BASE_URL}/`)
        alert('✅ Connected! ' + JSON.stringify(res.data))
      } catch (err) {
        this.error = `❌ Cannot connect: ${err.message}`
      }
    },
    
    async handleLogin() {
      try {
        this.error = null
        this.loading = true
        
        const response = await axios.post(`${API_BASE_URL}/login`, {
          username: this.username,
          password: this.password
        })
        
        if (response.data.success) {
          localStorage.setItem('token', response.data.token)
          this.$router.push('/admin')
        } else {
          throw new Error(response.data.message || 'Login failed')
        }
        
      } catch (err) {
        this.error = err.response?.data?.message || err.message
      } finally {
        this.loading = false
      }
    }
  }
}
</script>