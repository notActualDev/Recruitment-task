<script setup>
import { ref } from 'vue'

const password = ref("")
const message = ref("")

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

  </div>
</template>