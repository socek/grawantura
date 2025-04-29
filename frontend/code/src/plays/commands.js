import colors from '@/base/colors'
import { jwtCallWithErrorHandling } from "@/auth/calls"
import { playsUrl, hostUrl } from '@/base/urls'

export const createPlay = async (row) => {
  return await jwtCallWithErrorHandling(
    {
      "url": playsUrl(row.gameId),
      "method": "PUT",
      "data": {
        "name": row.name,
      }
    },
    {
      "success": "Row created!",
      "failed": "Row creation failed.",
    }
  )
}

export const updatePlay = async (row) => {
  return await jwtCallWithErrorHandling(
    {
      "url": playsUrl(row.gameId),
      "method": "PATCH",
      "data": {
        "game_id": row.game_id,
        "play_id": row.playId,
        "name": row.name,
      },
    },
    {
      "success": "Row updated!",
      "failed": "Row update failed.",
    }
  )
}

export const deletePlay = async (gameId, playId) => {
  return await jwtCallWithErrorHandling(
    {
      "url": playsUrl(gameId),
      "method": "DELETE",
      "data": {
        "play_id": playId,
      },
    },
    {
      "success": "Row deleted!",
      "failed": "Row delete failed.",
    }
  )
}

export const drawQuestion = async (playId) => {
  return await jwtCallWithErrorHandling(
    {
      "url": hostUrl(playId, "draw_question"),
      "method": "POST",
    },
    {
      "failed": "Draw failed.",
    },
    (result, notify) => {
      if(result.data.status == "fail") {
        notify({
          message: `Draw failed: ${result.data.description}.`,
          color: colors.fail,
        })
      } else {
        notify({
          message: "Draw succeed!",
          color: colors.success,
        })
      }
      return result
    }
  )
}

export default {
  createPlay,
  updatePlay,
  deletePlay,
  drawQuestion,
}
