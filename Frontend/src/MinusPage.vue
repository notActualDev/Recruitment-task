<script setup>
import { ref } from 'vue'

const counter = ref(420)

function minusOne() {
  counter.value--
}
</script>

<template>
  <div>
    <h1>MinusCounter: {{ counter }}</h1>
    <button @click="minusOne">-1</button>

    <br><br>

    <router-link to="/">
      Go to plus page
    </router-link>
  </div>
</template>