<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const message = ref('')
const loading = ref(false)

const router = useRouter()
const backendUrl = import.meta.env.VITE_BACKEND_URL

async function login() {
  message.value = ''

  if (!email.value || !password.value) {
    message.value = 'Wpisz email i hasło'
    return
  }

  loading.value = true

  try {
    const response = await fetch(`${backendUrl}/Users/Login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        Email: email.value,
        Password: password.value
      })
    })

    const data = await response.json()

    if (!response.ok) {
      message.value = data.detail || 'Logowanie nie powiodło się'
      return
    }

    const token = data.Token

    localStorage.setItem('userToken', token)
    localStorage.setItem('userEmail', email.value)

    router.push('/userHome')
  } catch (error) {
    message.value = 'Błąd połączenia z backendem'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="page">
    <div class="login-box">
      <h1>Login</h1>

      <input
          v-model="email"
          type="email"
          placeholder="Email"
          class="input"
      />

      <input
          v-model="password"
          type="password"
          placeholder="Hasło"
          class="input"
          @keyup.enter="login"
      />

      <button class="button" @click="login" :disabled="loading">
        {{ loading ? 'Logowanie...' : 'LOGIN' }}
      </button>

      <p v-if="message" class="message">
        {{ message }}
      </p>
    </div>
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #111;
  color: white;
  font-family: Arial, sans-serif;
}

.login-box {
  width: 100%;
  max-width: 420px;
  padding: 30px;
  border: 1px solid white;
  border-radius: 16px;
  background: #1a1a1a;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.input {
  padding: 12px;
  border-radius: 10px;
  border: 1px solid #666;
  background: #222;
  color: white;
  font-size: 16px;
}

.input::placeholder {
  color: #aaa;
}

.button {
  padding: 12px;
  border: none;
  border-radius: 10px;
  background: white;
  color: black;
  font-weight: bold;
  cursor: pointer;
  font-size: 16px;
}

.button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.message {
  margin: 0;
  color: #ff8080;
}
</style>