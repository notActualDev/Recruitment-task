<script setup>
import { ref } from 'vue'

const counter = ref(420)

function addOne() {
  counter.value++
}
</script>

<template>
  <div>
    <h1>Counter: {{ counter }}</h1>
    <button @click="addOne">+1</button>

    <br><br>

    <router-link to="/minus">
      Go to minus page
    </router-link>
  </div>
</template>