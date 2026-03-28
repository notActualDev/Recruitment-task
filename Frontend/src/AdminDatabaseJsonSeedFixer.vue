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



    <!-- CORRECT -->

    <div v-if="correctRecords.length" class="section">

      <h2 class="correct-title">Correct records</h2>

      <div class="actions">
        <button @click="selectAllCorrect">Select all</button>
        <button @click="deselectAllCorrect">Deselect all</button>
      </div>

      <div
          v-for="record in correctRecords"
          :key="record.id"
          class="record-card correct"
      >

        <div class="checkbox">
          <input type="checkbox" v-model="record.selected" />
        </div>

        <div class="record-fields">

          <div class="field"><span>ID</span>{{ record.id }}</div>
          <div class="field"><span>Name</span>{{ record.name }}</div>

          <div class="field"><span>Brand</span>{{ record.brand }}</div>
          <div class="field"><span>fixedBrand</span>{{ record.fixedBrand }}</div>

          <div class="field"><span>purchaseDate</span>{{ record.purchaseDate }}</div>
          <div class="field"><span>fixedPurchaseDate</span>{{ record.fixedPurchaseDate }}</div>

          <div class="field"><span>Status</span>{{ record.status }}</div>
          <div class="field"><span>fixedStatus</span>{{ record.fixedStatus }}</div>

          <div class="field"><span>assignedTo</span>{{ record.assignedTo }}</div>

          <div class="field"><span>notes</span>{{ record.notes }}</div>

          <div class="field"><span>history</span>{{ record.history }}</div>

          <div class="field"><span>needsAttention</span>{{ record.needsAttention }}</div>

          <div class="field"><span>attentionNotes</span>{{ record.attentionNotes }}</div>

        </div>

      </div>

    </div>



    <!-- ATTENTION -->

    <div v-if="attentionRecords.length" class="section">

      <h2 class="attention-title">Records that need attention</h2>

      <div class="actions">
        <button @click="selectAllAttention">Select all</button>
        <button @click="deselectAllAttention">Deselect all</button>
      </div>

      <div
          v-for="record in attentionRecords"
          :key="record.id"
          class="record-card attention"
      >

        <div class="checkbox">
          <input type="checkbox" v-model="record.selected" />
        </div>

        <div class="record-fields">

          <div class="field"><span>ID</span>{{ record.id }}</div>
          <div class="field"><span>Name</span>{{ record.name }}</div>

          <div class="field"><span>Brand</span>{{ record.brand }}</div>
          <div class="field"><span>fixedBrand</span>{{ record.fixedBrand }}</div>

          <div class="field"><span>purchaseDate</span>{{ record.purchaseDate }}</div>
          <div class="field"><span>fixedPurchaseDate</span>{{ record.fixedPurchaseDate }}</div>

          <div class="field"><span>Status</span>{{ record.status }}</div>
          <div class="field"><span>fixedStatus</span>{{ record.fixedStatus }}</div>

          <div class="field"><span>assignedTo</span>{{ record.assignedTo }}</div>

          <div class="field"><span>notes</span>{{ record.notes }}</div>

          <div class="field"><span>history</span>{{ record.history }}</div>

          <div class="field"><span>needsAttention</span>{{ record.needsAttention }}</div>

          <div class="field"><span>attentionNotes</span>{{ record.attentionNotes }}</div>

        </div>

      </div>

    </div>

  </div>

</template>

<style scoped>

.container {
  max-width: 1400px;
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


/* CARD STYLE (Stripe-like) */

.record-card {

  display: flex;

  gap: 20px;

  padding: 20px;

  margin-top: 12px;

  background: #050505;

  border-radius: 8px;

  transition: all 0.2s;

}

.record-card:hover {

  background: #0f0f0f;

  transform: translateY(-1px);

  box-shadow: 0 0 12px rgba(0,0,0,0.6);

}

.correct {
  border: 4px solid #00ff88;
}

.attention {
  border: 4px solid yellow;
}

.checkbox {
  padding-top: 6px;
}


/* FULL WIDTH GRID */

.record-fields {

  display: grid;

  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));

  gap: 14px;

  width: 100%;

}


/* FIELD CARD */

.field {

  background: #111;

  padding: 10px;

  border-radius: 6px;

  display: flex;

  flex-direction: column;

}

.field span {

  font-size: 11px;

  color: #888;

  margin-bottom: 3px;

}

.field {

  font-size: 14px;

}

</style>