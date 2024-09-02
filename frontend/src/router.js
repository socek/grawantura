import { createWebHashHistory, createRouter } from 'vue-router'

import Home from './components/Home.vue'
import GamePanel from './components/GamePanel.vue'
import EditorMain from './EditorPanel/EditorMain.vue'
import Auth from './Auth/Auth.vue'
import Account from './Auth/Account.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/game/:gameId', component: GamePanel},
  { path: '/editor', component: EditorMain},
  { path: '/login', component: Auth},
  { path: '/account', component: Account},
]

export default createRouter({
  history: createWebHashHistory(),
  routes,
})
