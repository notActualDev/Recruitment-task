<script setup>
import { ref, onMounted } from 'vue'

const users = ref([])
const email = ref('')
const password = ref('')

const apiUrl = import.meta.env.VITE_BACKEND_URL

const token = localStorage.getItem("adminToken")

async function loadUsers() {

  const response = await fetch(`${apiUrl}/Users/GetAllUsers`, {
    headers: {
      "admin-token": token
    }
  })

  if (!response.ok) {
    alert("Cannot load users")
    return
  }

  users.value = await response.json()
}

async function createUser() {

  const response = await fetch(`${apiUrl}/Users/CreateUser`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      "admin-token": token
    },
    body: JSON.stringify({
      Email: email.value,
      Password: password.value
    })
  })

  if (!response.ok) {
    alert("Cannot create user")
    return
  }

  email.value = ''
  password.value = ''

  await loadUsers()
}

onMounted(() => {
  loadUsers()
})
</script>


<template>

  <div class="container">

    <h1>Users management</h1>

    <div class="create">

      <h2>Create user</h2>

      <input
          v-model="email"
          placeholder="Email"
      />

      <input
          v-model="password"
          type="password"
          placeholder="Password"
      />

      <button @click="createUser">
        Create user
      </button>

    </div>

    <div class="users">

      <h2>Users</h2>

      <button @click="loadUsers">
        Refresh
      </button>

      <table>

        <thead>
        <tr>
          <th>ID</th>
          <th>Email</th>
          <th>Created</th>
        </tr>
        </thead>

        <tbody>

        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.created_at }}</td>
        </tr>

        </tbody>

      </table>

    </div>

  </div>

</template>


<style>

.container {
  max-width: 800px;
  margin: auto;
  font-family: Arial;
}

.create {
  margin-bottom: 20px;
}

input {
  display: block;
  margin: 6px 0;
  padding: 6px;
}

button {
  padding: 6px 12px;
  margin: 6px 0;
}

table {
  width: 100%;
  border-collapse: collapse;
}

td, th {
  border: 1px solid #ccc;
  padding: 6px;
}

</style>