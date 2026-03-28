<script setup>
import { ref } from 'vue'

const jsonInput = ref("")
const result = ref(null)
const loading = ref(false)
const error = ref(null)

const backendUrl = import.meta.env.VITE_BACKEND_URL

async function fixJson() {

  error.value = null
  result.value = null

  const token = localStorage.getItem("adminToken")

  if (!token) {
    error.value = "Admin token not found"
    return
  }

  loading.value = true

  try {

    const response = await fetch(`${backendUrl}/JsonRepair/Repair`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "admin-token": token
      },
      body: JSON.stringify({
        corruptedJson: jsonInput.value
      })
    })

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`)
    }

    const data = await response.json()

    result.value = data

  } catch (e) {

    error.value = e.message

  } finally {

    loading.value = false

  }
}
</script>

<template>

  <div class="container">

    <h1>Admin JSON Seed Fixer</h1>

    <textarea
        v-model="jsonInput"
        placeholder="Paste corrupted JSON here..."
        class="json-input"
    ></textarea>

    <button
        @click="fixJson"
        class="fix-button"
    >
      FIX
    </button>

    <div v-if="loading" class="loading">
      Processing with LLM...
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div v-if="result" class="result-container">

      <h2>LLM Result</h2>

      <pre class="result">
{{ JSON.stringify(result, null, 2) }}
    </pre>

    </div>

  </div>

</template>

<style scoped>

.container {
  max-width: 1000px;
  margin: auto;
  padding: 30px;
  font-family: Arial;
}

.json-input {
  width: 100%;
  height: 250px;
  font-family: monospace;
  font-size: 14px;
  padding: 10px;
  resize: vertical;
  overflow-y: scroll;
}

.fix-button {
  margin-top: 15px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

.loading {
  margin-top: 20px;
  color: #444;
}

.error {
  margin-top: 20px;
  color: red;
}

.result-container {
  margin-top: 30px;
}

.result {
  background: #111;
  color: #00ff88;
  padding: 20px;
  overflow-x: auto;
  white-space: pre-wrap;
}

</style>