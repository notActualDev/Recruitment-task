<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const userEmail = computed(() => {
  return localStorage.getItem('userEmail') || ''
})

function logout() {
  localStorage.removeItem('userToken')
  localStorage.removeItem('userEmail')
  router.push('/userLoginView')
}
</script>

<template>
  <div class="page">
    <div class="box">
      <h1>User panel</h1>
      <p>Zalogowany email:</p>
      <p class="email">{{ userEmail }}</p>

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
  max-width: 500px;
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

.button {
  padding: 12px 20px;
  border: none;
  border-radius: 10px;
  background: white;
  color: black;
  font-weight: bold;
  cursor: pointer;
}
</style>