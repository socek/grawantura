import { createWebHistory, createRouter } from 'vue-router'

import Home from './components/Home.vue'
import GamePanel from './components/GamePanel.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/game/:gameId', component: GamePanel},
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
