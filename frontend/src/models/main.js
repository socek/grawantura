import { createStore } from 'vuex'
import games from './games'

// Create a new store instance.
export default createStore({
  modules: {
    games: games,
  }
})

