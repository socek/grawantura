import { createWebHashHistory, createRouter } from 'vue-router'

import Home from './components/Home.vue'
import GamePanel from './components/GamePanel.vue'
import EditorMain from './EditorPanel/EditorMain.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/game/:gameId', component: GamePanel},
  { path: '/editor', component: EditorMain},
]

export default createRouter({
  history: createWebHashHistory(),
  routes,
})
