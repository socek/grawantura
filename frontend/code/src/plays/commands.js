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

export const changeView = async (playId, name) => {
  return await jwtCallWithErrorHandling(
    {
      "url": hostUrl(playId, "change_view"),
      "method": "POST",
      "data": {
        "name": name,
      }
    },
    {
      "success": "View changed!",
      "failed": "Draw failed.",
    },
  )
}

export const startGame = async (playId, money) => {
  return await jwtCallWithErrorHandling(
    {
      "url": hostUrl(playId, "start"),
      "method": "POST",
      "data": {
        "money": money
      }
    },
    {
      "success": "Game started!",
      "failed": "Game start failed.",
    },
  )
}

export const endAuction = async (playId, money) => {
  return await jwtCallWithErrorHandling(
    {
      "url": hostUrl(playId, "end_auction"),
      "method": "POST",
      "data": {
        "money": money
      }
    },
    {
      "success": "Auction finished!",
      "failed": "Auction end failed.",
    },
  )
}

export const addHint = async (playId, change, money) => {
  return await jwtCallWithErrorHandling(
    {
      "url": hostUrl(playId, "hint"),
      "method": "POST",
      "data": {
        "change": change,
        "money": money,
      }
    },
    {
      "success": "Hint added!",
      "failed": "Hint add failed.",
    },
  )
}

export const useHint = async (playId, teamId) => {
  const change = {}
  change[teamId] = -1
  return await jwtCallWithErrorHandling(
    {
      "url": hostUrl(playId, "hint"),
      "method": "POST",
      "data": {
        "change": change,
        "money": {},
      }
    },
    {
      "success": "Hint added!",
      "failed": "Hint add failed.",
    },
  )
}

export const answer = async (playId, success) => {
  return await jwtCallWithErrorHandling(
    {
      "url": hostUrl(playId, "answer"),
      "method": "POST",
      "data": {
        "success": success,
      }
    },
    {
      "success": "Answer saved!",
      "failed": "Answer save failed.",
    },
  )
}

export const deleteEvent = async (playId, eventId) => {
  return await jwtCallWithErrorHandling(
    {
      "url": hostUrl(playId, "event"),
      "method": "DELETE",
      "data": {
        "event_id": eventId,
      },
    },
    {
      "success": "Row deleted!",
      "failed": "Row delete failed.",
    }
  )
}

export default {
  createPlay,
  updatePlay,
  deletePlay,
  drawQuestion,
  changeView,
  startGame,
  endAuction,
  addHint,
  useHint,
  answer,
  deleteEvent,
}
