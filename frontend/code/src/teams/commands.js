import { useToast } from 'vuestic-ui'
import colors from '@/base/colors'
import { jwtCallWithErrorHandling } from "@/auth/calls"
import { teamsUrl } from '@/base/urls'

export const createTeam = async (row) => {
  return await jwtCallWithErrorHandling(
    {
      "url": teamsUrl(row.playId),
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

export const updateTeam = async (row) => {
  return await jwtCallWithErrorHandling(
    {
      "url": teamsUrl(row.playId),
      "method": "PATCH",
      "data": {
        "play_id": row.playId,
        "team_id": row.teamId,
        "name": row.name,
      },
    },
    {
      "success": "Row updated!",
      "failed": "Row update failed.",
    }
  )
}

export const deleteTeam = async (playId, teamId) => {
  return await jwtCallWithErrorHandling(
    {
      "url": teamsUrl(playId),
      "method": "DELETE",
      "data": {
        "team_id": teamId,
      },
    },
    {
      "success": "Row deleted!",
      "failed": "Row delete failed.",
    }
  )
}

export default {
  createTeam,
  updateTeam,
  deleteTeam,
}
