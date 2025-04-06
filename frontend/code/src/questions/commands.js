import { useToast } from 'vuestic-ui'
import colors from '@/base/colors'
import jwtCall from "@/auth/calls"

const url = (gameId) => `/api/games/${gameId}/questions`
const { init: notify } = useToast()

const createQuestion = async (row) => {
  try {
    await jwtCall({
      "url": url(row.gameId),
      "method": "PUT",
      "data": {
        "question": row.question,
        "answer": row.answer,
        "hints": row.hints,
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

const editQuestion = async (row) => {
  try {
    await jwtCall({
      "url": url(row.gameId),
      "method": "PATCH",
      "data": {
        "game_id": row.game_id,
        "question_id": row.questionId,
        "question": row.question,
        "answer": row.answer,
        "hints": row.hints,
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

const deleteQuestion = async (gameId, questionId) => {
  try {
    await jwtCall({
      "url": url(gameId),
      "method": "DELETE",
      "data": {
        "question_id": questionId,
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
  createQuestion,
  editQuestion,
  deleteQuestion,
}
