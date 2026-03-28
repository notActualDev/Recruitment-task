<script setup>
import { ref, computed } from 'vue'

const jsonInput = ref("")
const records = ref([])
const loading = ref(false)
const error = ref(null)

const correctOpen = ref(true)
const attentionOpen = ref(true)

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
    />

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

      <div class="section-header correct-border">

        <h2>Correct records</h2>

        <div class="section-buttons">

          <button @click="correctOpen = !correctOpen">
            {{ correctOpen ? "Collapse" : "Expand" }}
          </button>

          <button @click="selectAllCorrect">Select all</button>
          <button @click="deselectAllCorrect">Deselect all</button>

        </div>

      </div>

      <div v-if="correctOpen">

        <div
            v-for="record in correctRecords"
            :key="record.id"
            class="record-card correct"
        >

          <input type="checkbox" v-model="record.selected" class="checkbox" />

          <div class="record-fields">

            <div class="field"><b>ID</b>{{ record.id }}</div>
            <div class="field"><b>Name</b>{{ record.name }}</div>

            <div class="field"><b>Brand</b>{{ record.brand }}</div>
            <div class="field"><b>fixedBrand</b>{{ record.fixedBrand }}</div>

            <div class="field"><b>purchaseDate</b>{{ record.purchaseDate }}</div>
            <div class="field"><b>fixedPurchaseDate</b>{{ record.fixedPurchaseDate }}</div>

            <div class="field"><b>Status</b>{{ record.status }}</div>
            <div class="field"><b>fixedStatus</b>{{ record.fixedStatus }}</div>

            <div class="field"><b>assignedTo</b>{{ record.assignedTo }}</div>

            <div class="field"><b>notes</b>{{ record.notes }}</div>

            <div class="field"><b>history</b>{{ record.history }}</div>

            <div class="field"><b>needsAttention</b>{{ record.needsAttention }}</div>

            <div class="field"><b>attentionNotes</b>{{ record.attentionNotes }}</div>

          </div>

        </div>

      </div>

    </div>



    <!-- ATTENTION -->

    <div v-if="attentionRecords.length" class="section">

      <div class="section-header attention-border">

        <h2>Records that need attention</h2>

        <div class="section-buttons">

          <button @click="attentionOpen = !attentionOpen">
            {{ attentionOpen ? "Collapse" : "Expand" }}
          </button>

          <button @click="selectAllAttention">Select all</button>
          <button @click="deselectAllAttention">Deselect all</button>

        </div>

      </div>

      <div v-if="attentionOpen">

        <div
            v-for="record in attentionRecords"
            :key="record.id"
            class="record-card attention"
        >

          <input type="checkbox" v-model="record.selected" class="checkbox" />

          <div class="record-fields">

            <div class="field"><b>ID</b>{{ record.id }}</div>
            <div class="field"><b>Name</b>{{ record.name }}</div>

            <div class="field"><b>Brand</b>{{ record.brand }}</div>
            <div class="field"><b>fixedBrand</b>{{ record.fixedBrand }}</div>

            <div class="field"><b>purchaseDate</b>{{ record.purchaseDate }}</div>
            <div class="field"><b>fixedPurchaseDate</b>{{ record.fixedPurchaseDate }}</div>

            <div class="field"><b>Status</b>{{ record.status }}</div>
            <div class="field"><b>fixedStatus</b>{{ record.fixedStatus }}</div>

            <div class="field"><b>assignedTo</b>{{ record.assignedTo }}</div>

            <div class="field"><b>notes</b>{{ record.notes }}</div>

            <div class="field"><b>history</b>{{ record.history }}</div>

            <div class="field"><b>needsAttention</b>{{ record.needsAttention }}</div>

            <div class="field"><b>attentionNotes</b>{{ record.attentionNotes }}</div>

          </div>

        </div>

      </div>

    </div>

  </div>

</template>

<style scoped>

.container{

  width:100vw;
  min-height:100vh;

  padding:30px;

  background:#0b0b0b;
  color:white;

  font-family:Arial;

  box-sizing:border-box;

}

.section{
  margin-top:40px;
}

.section-header{
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding:10px;
  margin-bottom:10px;
}

.correct-border{
  border-left:6px solid #00ff88;
}

.attention-border{
  border-left:6px solid yellow;
}

.section-buttons button{
  margin-left:8px;
  padding:6px 12px;
  cursor:pointer;
}

.json-input{
  width:100%;
  height:200px;
  background:#111;
  color:#00ff88;
  border:1px solid #333;
  padding:10px;
  font-family:monospace;
}

.fix-button{
  margin-top:10px;
  padding:10px 20px;
  cursor:pointer;
}

.record-card{
  display:flex;
  gap:15px;
  margin-top:12px;
  padding:18px;
  background:#050505;
  border-radius:8px;
  transition:0.2s;
}

.record-card:hover{
  background:#0f0f0f;
  box-shadow:0 0 12px rgba(0,0,0,0.6);
}

.correct{
  border:3px solid #00ff88;
}

.attention{
  border:3px solid yellow;
}

.checkbox{
  margin-top:5px;
}

.record-fields{

  display:grid;

  /* TERAZ NAPRAWDĘ WYPEŁNIA CAŁĄ SZEROKOŚĆ */

  grid-template-columns: repeat(auto-fit,minmax(420px,1fr));

  gap:10px;

  width:100%;

}

.field{
  background:#111;
  padding:8px 10px;
  border-radius:6px;

  display:flex;
  flex-direction:column;

  font-size:13px;
}

.field b{
  font-size:10px;
  color:#999;
  margin-bottom:3px;
}

</style>