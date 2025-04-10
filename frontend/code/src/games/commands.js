import { useToast } from 'vuestic-ui'

import useAuthStore from "@/auth/store"
import colors from '@/base/colors'
import jwtCall from "@/auth/calls"
import { gamesUrl } from '@/base/urls'

const { init: notify } = useToast()

export const createGame = async (row) => {
  try {
    await jwtCall({
      "url": gamesUrl(),
      "method": "PUT",
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
}

export const editGame = async (row) => {
  try {
    await jwtCall({
      "url": gamesUrl(),
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
}

export const deleteGame = async (game_id) => {
  try {
    await jwtCall({
      "url": gamesUrl(),
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
}

export default {
  createGame,
  editGame,
  deleteGame,
}
