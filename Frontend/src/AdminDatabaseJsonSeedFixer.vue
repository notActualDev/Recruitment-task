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

function selectAllCorrect() {
  correctRecords.value.forEach(r => r.selected = true)
}

function deselectAllCorrect() {
  correctRecords.value.forEach(r => r.selected = false)
}

function selectAllAttention() {
  attentionRecords.value.forEach(r => r.selected = true)
}

function deselectAllAttention() {
  attentionRecords.value.forEach(r => r.selected = false)
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


    <!-- CORRECT RECORDS -->

    <div v-if="correctRecords.length" class="section">

      <h2 class="correct-title">Correct records</h2>

      <div class="actions">
        <button @click="selectAllCorrect">Select all</button>
        <button @click="deselectAllCorrect">Deselect all</button>
      </div>

      <div
          v-for="record in correctRecords"
          :key="record.id"
          class="record-bar correct"
      >

        <input type="checkbox" v-model="record.selected" />

        <div class="record-fields">

          <div><b>ID:</b> {{ record.id }}</div>
          <div><b>Name:</b> {{ record.name }}</div>

          <div><b>Brand:</b> {{ record.brand }}</div>
          <div><b>fixedBrand:</b> {{ record.fixedBrand }}</div>

          <div><b>purchaseDate:</b> {{ record.purchaseDate }}</div>
          <div><b>fixedPurchaseDate:</b> {{ record.fixedPurchaseDate }}</div>

          <div><b>Status:</b> {{ record.status }}</div>
          <div><b>fixedStatus:</b> {{ record.fixedStatus }}</div>

          <div><b>assignedTo:</b> {{ record.assignedTo }}</div>

          <div><b>notes:</b> {{ record.notes }}</div>

          <div><b>history:</b> {{ record.history }}</div>

          <div><b>needsAttention:</b> {{ record.needsAttention }}</div>

          <div><b>attentionNotes:</b> {{ record.attentionNotes }}</div>

        </div>

      </div>

    </div>



    <!-- ATTENTION RECORDS -->

    <div v-if="attentionRecords.length" class="section">

      <h2 class="attention-title">Records that need attention</h2>

      <div class="actions">
        <button @click="selectAllAttention">Select all</button>
        <button @click="deselectAllAttention">Deselect all</button>
      </div>

      <div
          v-for="record in attentionRecords"
          :key="record.id"
          class="record-bar attention"
      >

        <input type="checkbox" v-model="record.selected" />

        <div class="record-fields">

          <div><b>ID:</b> {{ record.id }}</div>
          <div><b>Name:</b> {{ record.name }}</div>

          <div><b>Brand:</b> {{ record.brand }}</div>
          <div><b>fixedBrand:</b> {{ record.fixedBrand }}</div>

          <div><b>purchaseDate:</b> {{ record.purchaseDate }}</div>
          <div><b>fixedPurchaseDate:</b> {{ record.fixedPurchaseDate }}</div>

          <div><b>Status:</b> {{ record.status }}</div>
          <div><b>fixedStatus:</b> {{ record.fixedStatus }}</div>

          <div><b>assignedTo:</b> {{ record.assignedTo }}</div>

          <div><b>notes:</b> {{ record.notes }}</div>

          <div><b>history:</b> {{ record.history }}</div>

          <div><b>needsAttention:</b> {{ record.needsAttention }}</div>

          <div><b>attentionNotes:</b> {{ record.attentionNotes }}</div>

        </div>

      </div>

    </div>

  </div>

</template>

<style scoped>

.container {
  max-width: 1200px;
  margin: auto;
  padding: 30px;
  font-family: Arial;
  background: #0b0b0b;
  color: white;
}

.section {
  margin-top: 40px;
}

.correct-title {
  color: #00ff88;
}

.attention-title {
  color: yellow;
}

.json-input {
  width: 100%;
  height: 220px;
  font-family: monospace;
  padding: 10px;
  background: #111;
  color: #00ff88;
  border: 1px solid #333;
}

.fix-button {
  margin-top: 15px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

.actions {
  margin-bottom: 15px;
}

.actions button {
  margin-right: 10px;
  padding: 6px 12px;
  cursor: pointer;
}

.record-bar {

  display: flex;
  align-items: flex-start;
  gap: 15px;

  background: black;
  padding: 15px;
  margin-top: 10px;

  border-radius: 6px;
}

.correct {
  border: 4px solid #00ff88;
}

.attention {
  border: 4px solid yellow;
}

.record-fields {

  display: grid;
  grid-template-columns: repeat(4, auto);
  gap: 15px;

  font-size: 14px;
}

.record-fields b {
  color: #00d0ff;
}

</style>