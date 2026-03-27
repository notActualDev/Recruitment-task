<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const password = ref("")
const message = ref("")
const router = useRouter()

async function login() {

  const backendUrl = import.meta.env.VITE_BACKEND_URL

  try {

    const response = await fetch(
        `${backendUrl}/admin/login?password=${encodeURIComponent(password.value)}`,
        { method: "POST" }
    )

    if (!response.ok) {
      message.value = "Logowanie się nie powiodło"
      return
    }

    const data = await response.json()

    const token = data.token

    if (token) {

      // zapis tokena
      localStorage.setItem("adminToken", token)

      // przejście na panel admina
      router.push("/adminMainScreen")

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