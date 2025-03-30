import axios from 'axios';
const { init: notify } = useToast()
import { useToast } from 'vuestic-ui'
import useGamesStore from './store'
import colors from '@/base/colors'

const GAMES_URL = "/api/games"
const gamesStore = useGamesStore()

const createGame = async (row) => {
  try {
    await axios.post(GAMES_URL,
      {
        name: row.name
     }
    )
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
  await gamesStore.fetch(true)
}

const editGame = async (row) => {
  try {
    await axios.patch(
      GAMES_URL,
      {
        "game_id": row.game_id,
        "name": row.name,
      }
    )
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
  await gamesStore.fetch(true)
}

const deleteGame = async (game_id) => {
  try {
    await axios.delete(
      GAMES_URL,
      {
        data: {
          "game_id": game_id,
        }
      }
    )
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
  await gamesStore.fetch(true)
}

export default {
  createGame,
  editGame,
  deleteGame,
}
