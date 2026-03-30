<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const backendUrl = import.meta.env.VITE_BACKEND_URL

const userEmail = computed(() => {
  return localStorage.getItem('userEmail') || ''
})

const hardware = ref([])
const error = ref(null)

function getToken() {
  return localStorage.getItem('userToken')
}

async function loadHardware() {

  error.value = null

  try {

    const response = await fetch(
        `${backendUrl}/Hardware/GetAllAvailableHardwareForUserToken`,
        {
          headers: {
            "user-token": getToken()
          }
        }
    )

    if (!response.ok) {
      throw new Error("Nie udało się pobrać sprzętu")
    }

    hardware.value = await response.json()

  } catch (e) {
    error.value = e.message
  }
}

function logout() {
  localStorage.removeItem('userToken')
  localStorage.removeItem('userEmail')
  router.push('/userLoginView')
}

onMounted(() => {
  loadHardware()
})
</script>

<template>
  <div class="page">
    <div class="box">

      <h1>User panel</h1>

      <p>Zalogowany email:</p>
      <p class="email">{{ userEmail }}</p>

      <h2>Dostępne urządzenia</h2>

      <div v-if="error" class="error">
        {{ error }}
      </div>

      <div v-if="hardware.length === 0">
        Brak dostępnych urządzeń
      </div>

      <table v-if="hardware.length > 0" class="table">
        <thead>
        <tr>
          <th>Nazwa</th>
          <th>Marka</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(item, index) in hardware" :key="index">
          <td>{{ item.Name }}</td>
          <td>{{ item.Brand }}</td>
        </tr>
        </tbody>
      </table>

      <button class="button" @click="logout">
        WYLOGUJ
      </button>

    </div>
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #111;
  color: white;
  font-family: Arial, sans-serif;
}

.box {
  width: 100%;
  max-width: 700px;
  padding: 30px;
  border: 1px solid white;
  border-radius: 16px;
  background: #1a1a1a;
  text-align: center;
}

.email {
  font-size: 22px;
  font-weight: bold;
  margin: 20px 0;
}

.table {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
}

.table th,
.table td {
  border-bottom: 1px solid #444;
  padding: 10px;
}

.table th {
  text-align: left;
}

.button {
  margin-top: 30px;
  padding: 12px 20px;
  border: none;
  border-radius: 10px;
  background: white;
  color: black;
  font-weight: bold;
  cursor: pointer;
}

.error {
  color: #ff6b6b;
  margin-top: 10px;
}
</style>