import { useToast } from 'vuestic-ui'
import useGamesStore from './store'
import useAuthStore from "@/auth/store"
import colors from '@/base/colors'
import jwtCall from "@/auth/calls"

const GAMES_URL = "/api/games"
const { init: notify } = useToast()
const gamesStore = useGamesStore()

const createGame = async (row) => {
  try {
    await jwtCall({
      "url": GAMES_URL,
      "method": "POST",
      "data": {
        name: row.name
      }
    })
  } catch(error) {
    notify({
      message: `Row save failed`,
      color: colors.fail,
    })
    throw error
  }

  notify({
    message: `Row saved!`,
    color: colors.success,
  })
  // await gamesStore.fetch(true)
}

const editGame = async (row) => {
  try {
    await jwtCall({
      "url": GAMES_URL,
      "method": "PATCH",
      "data": {
        "game_id": row.game_id,
        "name": row.name,
      },
    })
  } catch(error) {
    notify({
      message: `Row save failed`,
      color: colors.fail,
    })
    throw error
  }
  notify({
    message: `Row saved!`,
    color: colors.success,
  })
  // await gamesStore.fetch(true)
}

const deleteGame = async (game_id) => {
  try {
    await jwtCall({
      "url": GAMES_URL,
      "method": "DELETE",
      "data": {
        "game_id": game_id,
      },
    })
  } catch(error) {
    notify({
      message: `Row delete failed`,
      color: colors.fail,
    })
    throw error
  }
  notify({
    message: `Row deleted!`,
    color: colors.success,
  })
  // await gamesStore.fetch(true)
}

export default {
  createGame,
  editGame,
  deleteGame,
}
