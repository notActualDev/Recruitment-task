<script setup>
import { ref } from 'vue'

const counter = ref(420)
const text = ref('')

// adres backendu z Vercel Environment Variables
const backendUrl = import.meta.env.VITE_BACKEND_URL

function addOne() {
  counter.value++
}

async function getText() {
  try {
    const response = await fetch(`${backendUrl}/`)
    const data = await response.text()
    text.value = data
  } catch (error) {
    text.value = 'Error while fetching data'
  }
}

function clearText() {
  text.value = ''
}
</script>

<template>
  <div>
    <h1>AddCounter: {{ counter }}</h1>
    <button @click="addOne">+1</button>

    <br><br>

    <router-link to="/minus">
      Go to minus page
    </router-link>

    <br><br>

    <!-- pole wyświetlania tekstu -->
    <div style="border:1px solid black; padding:10px; min-height:50px;">
      {{ text }}
    </div>

    <br>

    <button @click="getText">Get</button>
    <button @click="clearText">Clear</button>
  </div>
</template>