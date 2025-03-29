import { createStore } from 'vuex'
import games from './games'
import auth from './auth'

// Create a new store instance.
export default createStore({
  modules: {
    games: games,
    auth: auth,
  }
})

