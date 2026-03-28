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

function selectAllCorrect(){
  correctRecords.value.forEach(r=>r.selected=true)
}

function deselectAllCorrect(){
  correctRecords.value.forEach(r=>r.selected=false)
}

function selectAllAttention(){
  attentionRecords.value.forEach(r=>r.selected=true)
}

function deselectAllAttention(){
  attentionRecords.value.forEach(r=>r.selected=false)
}

</script>


<template>

  <div class="page">

    <h1>Admin JSON Seed Fixer</h1>

    <textarea
        v-model="jsonInput"
        class="json-input"
    />

    <button @click="fixJson" class="fix-button">
      FIX
    </button>


    <div v-if="loading">Processing with LLM...</div>
    <div v-if="error">{{error}}</div>



    <!-- CORRECT -->

    <div v-if="correctRecords.length" class="section">

      <div class="section-header correct-border">

        <h2>Correct records</h2>

        <div>

          <button @click="correctOpen=!correctOpen">
            {{correctOpen?"Collapse":"Expand"}}
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

          <input type="checkbox" v-model="record.selected">

          <div class="fields">

            <div class="field"><b>ID</b>{{record.id}}</div>
            <div class="field"><b>Name</b>{{record.name}}</div>

            <div class="field"><b>Brand</b>{{record.brand}}</div>
            <div class="field"><b>fixedBrand</b>{{record.fixedBrand}}</div>

            <div class="field"><b>purchaseDate</b>{{record.purchaseDate}}</div>
            <div class="field"><b>fixedPurchaseDate</b>{{record.fixedPurchaseDate}}</div>

            <div class="field"><b>Status</b>{{record.status}}</div>
            <div class="field"><b>fixedStatus</b>{{record.fixedStatus}}</div>

            <div class="field"><b>assignedTo</b>{{record.assignedTo}}</div>

            <div class="field"><b>notes</b>{{record.notes}}</div>

            <div class="field"><b>history</b>{{record.history}}</div>

            <div class="field"><b>needsAttention</b>{{record.needsAttention}}</div>

            <div class="field"><b>attentionNotes</b>{{record.attentionNotes}}</div>

          </div>

        </div>

      </div>

    </div>



    <!-- ATTENTION -->

    <div v-if="attentionRecords.length" class="section">

      <div class="section-header attention-border">

        <h2>Records that need attention</h2>

        <div>

          <button @click="attentionOpen=!attentionOpen">
            {{attentionOpen?"Collapse":"Expand"}}
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

          <input type="checkbox" v-model="record.selected">

          <div class="fields">

            <div class="field"><b>ID</b>{{record.id}}</div>
            <div class="field"><b>Name</b>{{record.name}}</div>

            <div class="field"><b>Brand</b>{{record.brand}}</div>
            <div class="field"><b>fixedBrand</b>{{record.fixedBrand}}</div>

            <div class="field"><b>purchaseDate</b>{{record.purchaseDate}}</div>
            <div class="field"><b>fixedPurchaseDate</b>{{record.fixedPurchaseDate}}</div>

            <div class="field"><b>Status</b>{{record.status}}</div>
            <div class="field"><b>fixedStatus</b>{{record.fixedStatus}}</div>

            <div class="field"><b>assignedTo</b>{{record.assignedTo}}</div>

            <div class="field"><b>notes</b>{{record.notes}}</div>

            <div class="field"><b>history</b>{{record.history}}</div>

            <div class="field"><b>needsAttention</b>{{record.needsAttention}}</div>

            <div class="field"><b>attentionNotes</b>{{record.attentionNotes}}</div>

          </div>

        </div>

      </div>

    </div>

  </div>

</template>



<style scoped>

/* 🔧 NADPISANIE OGRANICZENIA VITE */
:global(#app){
  max-width:none;
  width:100%;
  margin:0;
  padding:0;
}

/* pełna szerokość strony */

.page{

  width:100%;
  padding:30px;

  background:#0b0b0b;
  color:white;

  font-family:Arial;

  box-sizing:border-box;

}

/* textarea */

.json-input{

  width:100%;
  height:200px;

  background:#111;
  color:#00ff88;

  border:1px solid #333;

  padding:10px;

  font-family:monospace;

  margin-bottom:10px;

}

.fix-button{

  padding:10px 20px;
  cursor:pointer;

  margin-bottom:30px;

}

/* sekcje */

.section{
  margin-top:40px;
}

.section-header{

  display:flex;
  justify-content:space-between;
  align-items:center;

  margin-bottom:10px;

}

.correct-border{
  border-left:6px solid #00ff88;
  padding-left:10px;
}

.attention-border{
  border-left:6px solid yellow;
  padding-left:10px;
}


/* rekord */

.record{

  display:flex;
  gap:15px;

  background:#050505;

  padding:15px;

  margin-top:10px;

  border-radius:6px;

}

.correct{
  border:3px solid #00ff88;
}

.attention{
  border:3px solid yellow;
}


/* 🔧 NAJWAŻNIEJSZE — SZEROKI UKŁAD PÓL */

.fields{

  display:grid;

  /* dużo kolumn -> rekord szeroki */

  grid-template-columns: repeat(6,1fr);

  gap:8px;

  width:100%;

}

/* pole */

.field{

  background:#111;

  padding:6px 8px;

  border-radius:4px;

  display:flex;
  flex-direction:column;

  font-size:12px;

}

.field b{

  font-size:9px;
  color:#999;

  margin-bottom:2px;

}

</style>