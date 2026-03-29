<script setup>
import { ref, computed } from 'vue'

const jsonInput = ref("")
const records = ref([])
const loading = ref(false)
const error = ref(null)

const correctOpen = ref(true)
const attentionOpen = ref(true)

const backendJson = ref(null)

const backendUrl = import.meta.env.VITE_BACKEND_URL

function isValidDate(date) {
  if (!date) return true

  const regex = /^\d{4}-\d{2}-\d{2}$/
  if (!regex.test(date)) return false

  const d = new Date(date)
  return !isNaN(d.getTime())
}

function changed(record, field) {
  return record[field] !== record["initial" + field]
}

function recordHasInvalidDate(record) {
  return !isValidDate(record.acceptedPurchaseDate)
}

function normalizeNullableString(value) {
  if (value === null || value === undefined) return null
  if (typeof value !== "string") return value
  return value.trim() === "" ? null : value
}

async function fixJson() {
  error.value = null
  backendJson.value = null
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

    records.value = data.map(r => {
      const acceptedName = r.name ?? ""
      const acceptedBrand = r.fixedBrand ?? r.brand ?? ""
      const acceptedPurchaseDate = r.fixedPurchaseDate ?? r.purchaseDate ?? ""
      const acceptedStatus = r.fixedStatus ?? r.status ?? "Unknown"
      const acceptedAssignedTo = r.assignedTo ?? ""

      return {
        ...r,
        selected: false,

        acceptedName,
        acceptedBrand,
        acceptedPurchaseDate,
        acceptedStatus,
        acceptedAssignedTo,

        initialacceptedName: acceptedName,
        initialacceptedBrand: acceptedBrand,
        initialacceptedPurchaseDate: acceptedPurchaseDate,
        initialacceptedStatus: acceptedStatus,
        initialacceptedAssignedTo: acceptedAssignedTo
      }
    })
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
  correctRecords.value.forEach(r => {
    r.selected = true
  })
}

function deselectAllCorrect() {
  correctRecords.value.forEach(r => {
    r.selected = false
  })
}

function selectAllAttention() {
  attentionRecords.value.forEach(r => {
    r.selected = true
  })
}

function deselectAllAttention() {
  attentionRecords.value.forEach(r => {
    r.selected = false
  })
}

const hasInvalidDates = computed(() =>
    records.value.some(r => !isValidDate(r.acceptedPurchaseDate))
)

async function saveSelected() {
  error.value = null
  backendJson.value = null

  const token = localStorage.getItem("adminToken")

  if (!token) {
    error.value = "Admin token not found"
    return
  }

  const selected = records.value.filter(r => r.selected)

  const payload = {
    Records: selected.map(r => ({
      Name: normalizeNullableString(r.acceptedName),
      Brand: normalizeNullableString(r.acceptedBrand),
      PurchaseDate: normalizeNullableString(r.acceptedPurchaseDate),
      Status: r.acceptedStatus || "Unknown",
      AssignedTo: normalizeNullableString(r.acceptedAssignedTo),
      Notes: normalizeNullableString(r.notes),
      History: normalizeNullableString(r.history)
    }))
  }

  try {
    const response = await fetch(`${backendUrl}/SeedAcceptedRecords`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "admin-token": token
      },
      body: JSON.stringify(payload)
    })

    if (!response.ok) {
      const text = await response.text()
      throw new Error(`Backend error: ${response.status} ${text}`)
    }

    const data = await response.json()
    backendJson.value = JSON.stringify(data, null, 2)
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div class="page">
    <h1>Admin JSON Seed Fixer</h1>

    <textarea
        v-model="jsonInput"
        class="json-input"
        placeholder="Paste corrupted JSON here..."
    />

    <button @click="fixJson" class="fix-button">
      FIX
    </button>

    <div v-if="loading">Processing with LLM...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <!-- CORRECT -->
    <div v-if="correctRecords.length" class="section">
      <div class="section-header correct-border">
        <h2>Correct records</h2>

        <div>
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
            class="record correct"
        >
          <div class="checkbox-col">
            <input type="checkbox" v-model="record.selected">
          </div>

          <div class="record-body">
            <div class="record-warning" v-if="recordHasInvalidDate(record)">
              ⚠ Invalid date
            </div>

            <div class="fields">
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

            <div class="accepted-fields">
              <div
                  class="field editable"
                  :class="{ changed: changed(record, 'acceptedName') }"
              >
                <b>acceptedName</b>
                <input v-model="record.acceptedName">
              </div>

              <div
                  class="field editable"
                  :class="{ changed: changed(record, 'acceptedBrand') }"
              >
                <b>acceptedBrand</b>
                <input v-model="record.acceptedBrand">
              </div>

              <div
                  class="field editable"
                  :class="{
                  changed: changed(record, 'acceptedPurchaseDate'),
                  invalid: !isValidDate(record.acceptedPurchaseDate)
                }"
              >
                <b>acceptedPurchaseDate</b>
                <input v-model="record.acceptedPurchaseDate">
              </div>

              <div
                  class="field editable"
                  :class="{ changed: changed(record, 'acceptedStatus') }"
              >
                <b>acceptedStatus</b>
                <select v-model="record.acceptedStatus">
                  <option>Available</option>
                  <option>In Use</option>
                  <option>Repair</option>
                  <option>Unknown</option>
                </select>
              </div>

              <div
                  class="field editable"
                  :class="{ changed: changed(record, 'acceptedAssignedTo') }"
              >
                <b>acceptedAssignedTo</b>
                <input v-model="record.acceptedAssignedTo">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ATTENTION -->
    <div v-if="attentionRecords.length" class="section">
      <div class="section-header attention-border">
        <h2>Records that need attention</h2>

        <div>
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
            class="record attention"
        >
          <div class="checkbox-col">
            <input type="checkbox" v-model="record.selected">
          </div>

          <div class="record-body">
            <div class="record-warning" v-if="recordHasInvalidDate(record)">
              ⚠ Invalid date
            </div>

            <div class="fields">
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

            <div class="accepted-fields">
              <div
                  class="field editable"
                  :class="{ changed: changed(record, 'acceptedName') }"
              >
                <b>acceptedName</b>
                <input v-model="record.acceptedName">
              </div>

              <div
                  class="field editable"
                  :class="{ changed: changed(record, 'acceptedBrand') }"
              >
                <b>acceptedBrand</b>
                <input v-model="record.acceptedBrand">
              </div>

              <div
                  class="field editable"
                  :class="{
                  changed: changed(record, 'acceptedPurchaseDate'),
                  invalid: !isValidDate(record.acceptedPurchaseDate)
                }"
              >
                <b>acceptedPurchaseDate</b>
                <input v-model="record.acceptedPurchaseDate">
              </div>

              <div
                  class="field editable"
                  :class="{ changed: changed(record, 'acceptedStatus') }"
              >
                <b>acceptedStatus</b>
                <select v-model="record.acceptedStatus">
                  <option>Available</option>
                  <option>In Use</option>
                  <option>Repair</option>
                  <option>Unknown</option>
                </select>
              </div>

              <div
                  class="field editable"
                  :class="{ changed: changed(record, 'acceptedAssignedTo') }"
              >
                <b>acceptedAssignedTo</b>
                <input v-model="record.acceptedAssignedTo">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- SAVE -->
    <div class="save-section">
      <button
          @click="saveSelected"
          :disabled="hasInvalidDates"
          class="save-button"
      >
        SAVE SELECTED RECORDS
      </button>

      <div v-if="hasInvalidDates" class="save-warning">
        Cannot save while invalid dates exist
      </div>
    </div>

    <!-- BACKEND JSON -->
    <div v-if="backendJson" class="output-section">
      <h2>JSON z backendu</h2>
      <pre>{{ backendJson }}</pre>
    </div>
  </div>
</template>

<style scoped>
:global(#app) {
  max-width: none !important;
  width: 100vw;
  margin: 0;
  padding: 0;
}

.page {
  width: 100vw;
  padding: 30px;
  background: #0b0b0b;
  color: white;
  font-family: Arial;
  box-sizing: border-box;
}

.json-input {
  width: 100%;
  height: 200px;
  background: #111;
  color: #00ff88;
  border: 1px solid #333;
  padding: 10px;
  font-family: monospace;
  margin-bottom: 10px;
}

.fix-button {
  padding: 10px 20px;
  margin-bottom: 30px;
  cursor: pointer;
}

.error {
  color: #ff6b6b;
  margin-top: 12px;
}

.section {
  margin-top: 40px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.correct-border {
  border-left: 6px solid #00ff88;
  padding-left: 10px;
}

.attention-border {
  border-left: 6px solid yellow;
  padding-left: 10px;
}

.record {
  display: flex;
  gap: 15px;
  background: #050505;
  padding: 15px;
  margin-top: 10px;
  border-radius: 6px;
}

.correct {
  border: 3px solid #00ff88;
}

.attention {
  border: 3px solid yellow;
}

.checkbox-col {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
}

.checkbox-col input {
  transform: scale(1.6);
}

.record-body {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.record-warning {
  color: #ffcc00;
  font-size: 12px;
}

.fields {
  display: grid;
  grid-template-columns: repeat(8, minmax(120px, 1fr));
  gap: 8px;
}

.accepted-fields {
  display: grid;
  grid-template-columns: repeat(5, minmax(160px, 1fr));
  gap: 8px;
}

.field {
  background: #111;
  padding: 6px 8px;
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  font-size: 12px;
}

.field b {
  font-size: 9px;
  color: #999;
}

.editable {
  background: #1a1a1a;
}

.editable input,
.editable select {
  background: #222;
  color: white;
  border: 1px solid #444;
  padding: 4px;
}

.changed {
  background: #4d3f00;
}

.invalid {
  background: #4d0000;
}

.save-section {
  margin-top: 40px;
}

.save-button {
  padding: 12px 20px;
  font-size: 14px;
  cursor: pointer;
}

.save-warning {
  color: red;
  margin-top: 10px;
}

.output-section {
  margin-top: 40px;
}

pre {
  background: #111;
  padding: 20px;
  overflow: auto;
}
</style>