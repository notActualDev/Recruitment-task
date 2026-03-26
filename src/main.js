import './assets/main.css'

import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'

import App from './App.vue'
import AddPage from './AddPage.vue'
import MinusPage from './MinusPage.vue'

const routes = [
    { path: '/', component: AddPage },
    { path: '/minus', component: MinusPage }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

createApp(App).use(router).mount('#app')