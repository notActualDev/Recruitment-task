<script setup>
import { ref } from 'vue'

const password = ref("")
const message = ref("")
const debugInfo = ref("")

async function login() {

  const backendUrl = import.meta.env.VITE_BACKEND_URL

  try {

    const response = await fetch(
        `${backendUrl}/admin/login?password=${encodeURIComponent(password.value)}`,
        {
          method: "POST"
        }
    )

    const data = await response.json()

    // pokazujemy odpowiedź backendu
    debugInfo.value = JSON.stringify(data, null, 2)

    if (data.success) {
      message.value = "Logowanie powiodło się"
    } else {
      message.value = "Logowanie się nie powiodło"
    }

  } catch (error) {
    message.value = "Błąd połączenia z backendem"
  }

}
</script>


<template>
  <div>

    <h1>Admin Login</h1>

    <input
        type="password"
        v-model="password"
        placeholder="Wpisz hasło"
    />

    <button @click="login">
      LOGIN
    </button>

    <p>{{ message }}</p>

    <h3>Debug backend response:</h3>
    <pre>{{ debugInfo }}</pre>

  </div>
</template>