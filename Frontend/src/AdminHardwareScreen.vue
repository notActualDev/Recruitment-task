<script setup>

import { ref, onMounted } from "vue"

const backendUrl = import.meta.env.VITE_BACKEND_URL

const hardware = ref([])
const error = ref(null)

const form = ref({
  Name: "",
  Brand: "",
  PurchaseDate: "",
  Status: "Available",
  AssignedTo: "",
  Notes: "",
  History: ""
})

function getToken() {
  return localStorage.getItem("adminToken")
}

async function loadHardware() {

  error.value = null

  try {

    const response = await fetch(
        `${backendUrl}/Hardware/GetAllHardware`,
        {
          headers: {
            "admin-token": getToken()
          }
        }
    )

    if (!response.ok) {
      throw new Error("Failed to load hardware")
    }

    hardware.value = await response.json()

  } catch (e) {

    error.value = e.message

  }
}

async function createHardware() {

  error.value = null

  try {

    const response = await fetch(
        `${backendUrl}/Hardware/CreateHardware`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "admin-token": getToken()
          },
          body: JSON.stringify(form.value)
        }
    )

    if (!response.ok) {
      throw new Error("Create failed")
    }

    form.value = {
      Name: "",
      Brand: "",
      PurchaseDate: "",
      Status: "Available",
      AssignedTo: "",
      Notes: "",
      History: ""
    }

    await loadHardware()

  } catch (e) {

    error.value = e.message

  }
}

async function deleteHardware(id) {

  error.value = null

  try {

    const response = await fetch(
        `${backendUrl}/Hardware/DeleteHardware/${id}`,
        {
          method: "DELETE",
          headers: {
            "admin-token": getToken()
          }
        }
    )

    if (!response.ok) {
      throw new Error("Delete failed")
    }

    await loadHardware()

  } catch (e) {

    error.value = e.message

  }
}

async function updateHardware(item) {

  error.value = null

  try {

    const response = await fetch(
        `${backendUrl}/Hardware/UpdateHardware/${item.Id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "admin-token": getToken()
          },
          body: JSON.stringify(item)
        }
    )

    if (!response.ok) {
      throw new Error("Update failed")
    }

  } catch (e) {

    error.value = e.message

  }
}

onMounted(loadHardware)

</script>

<template>

  <div class="container">

    <h1>Hardware Admin</h1>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <h2>Add Hardware</h2>

    <div class="form">

      <input v-model="form.Name" placeholder="Name" />
      <input v-model="form.Brand" placeholder="Brand" />
      <input v-model="form.PurchaseDate" placeholder="PurchaseDate (YYYY-MM-DD)" />

      <select v-model="form.Status">
        <option>Available</option>
        <option>In Use</option>
        <option>Repair</option>
        <option>Unknown</option>
      </select>

      <input v-model="form.AssignedTo" placeholder="Assigned To" />
      <input v-model="form.Notes" placeholder="Notes" />
      <input v-model="form.History" placeholder="History" />

      <button @click="createHardware">
        Add
      </button>

    </div>

    <h2>Hardware List</h2>

    <table>

      <thead>
      <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Brand</th>
        <th>Status</th>
        <th>Assigned</th>
        <th>Notes</th>
        <th>History</th>
        <th>Actions</th>
      </tr>
      </thead>

      <tbody>

      <tr v-for="item in hardware" :key="item.Id">

        <td>{{ item.Id }}</td>

        <td>
          <input v-model="item.Name" />
        </td>

        <td>
          <input v-model="item.Brand" />
        </td>

        <td>
          <select v-model="item.Status">
            <option>Available</option>
            <option>In Use</option>
            <option>Repair</option>
            <option>Unknown</option>
          </select>
        </td>

        <td>
          <input v-model="item.AssignedTo" />
        </td>

        <td>
          <input v-model="item.Notes" />
        </td>

        <td>
          <input v-model="item.History" />
        </td>

        <td>

          <button @click="updateHardware(item)">
            Save
          </button>

          <button @click="deleteHardware(item.Id)">
            Delete
          </button>

        </td>

      </tr>

      </tbody>

    </table>

  </div>

</template>

<style>

.container{
  max-width:1400px;
  margin:auto;
  padding:30px;
  font-family:Arial;
}

table{
  width:100%;
  border-collapse:collapse;
  margin-top:20px;
}

td,th{
  border:1px solid #ccc;
  padding:8px;
}

.form input,
.form select{
  margin-right:10px;
  margin-bottom:10px;
}

.error{
  color:red;
  margin-bottom:20px;
}

</style>