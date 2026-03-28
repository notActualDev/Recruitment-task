<script setup>
import { ref, computed } from 'vue'

const jsonInput = ref("")
const records = ref([])
const loading = ref(false)
const error = ref(null)

const backendUrl = import.meta.env.VITE_BACKEND_URL

async function fixJson() {

  error.value = null
  records.value = []

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

    // zapisujemy rekordy
    records.value = data.map(r => ({
      ...r,
      selected: false
    }))

  } catch (e) {

    error.value = e.message

  } finally {

    loading.value = false

  }
}

const correctRecords = computed(() =>
    records.value.filter(r => !r.needsAttention)
)

const attentionRecords = computed(() =>
    records.value.filter(r => r.needsAttention)
)

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


    <!-- CORRECT RECORDS -->

    <div v-if="correctRecords.length">

      <h2>Correct records</h2>

      <div
          v-for="record in correctRecords"
          :key="record.id"
          class="record-bar"
      >

        <input
            type="checkbox"
            v-model="record.selected"
        />

        <div class="record-fields">

          <div><b>ID:</b> {{ record.id }}</div>
          <div><b>Name:</b> {{ record.name }}</div>
          <div><b>Brand:</b> {{ record.brand }}</div>
          <div><b>Purchase:</b> {{ record.purchaseDate }}</div>
          <div><b>Status:</b> {{ record.status }}</div>

        </div>

      </div>

    </div>



    <!-- ATTENTION RECORDS -->

    <div v-if="attentionRecords.length">

      <h2>Records that need attention</h2>

      <div
          v-for="record in attentionRecords"
          :key="record.id"
          class="record-bar attention"
      >

        <input
            type="checkbox"
            v-model="record.selected"
        />

        <div class="record-fields">

          <div><b>ID:</b> {{ record.id }}</div>
          <div><b>Name:</b> {{ record.name }}</div>
          <div><b>Brand:</b> {{ record.brand }}</div>
          <div><b>Purchase:</b> {{ record.purchaseDate }}</div>
          <div><b>Status:</b> {{ record.status }}</div>

          <div class="attention-note">
            ⚠ {{ record.attentionNotes }}
          </div>

        </div>

      </div>

    </div>

  </div>

</template>

<style scoped>

.container {
  max-width: 1100px;
  margin: auto;
  padding: 30px;
  font-family: Arial;
}

.json-input {
  width: 100%;
  height: 220px;
  font-family: monospace;
  padding: 10px;
}

.fix-button {
  margin-top: 15px;
  padding: 10px 20px;
  font-size: 16px;
}

.loading {
  margin-top: 20px;
}

.error {
  color: red;
  margin-top: 20px;
}

.record-bar {

  display: flex;
  align-items: flex-start;

  gap: 15px;

  background: #f4f4f4;

  padding: 15px;

  margin-top: 10px;

  border-radius: 6px;
}

.record-bar.attention {

  background: #ffe6e6;
}

.record-fields {

  display: grid;

  grid-template-columns: repeat(5, auto);

  gap: 20px;

  font-size: 14px;
}

.attention-note {

  grid-column: span 5;

  color: red;

  font-weight: bold;
}

</style>