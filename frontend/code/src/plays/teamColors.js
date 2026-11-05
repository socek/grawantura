// Colors for teams on the game screen (/play). A team keeps the same color
// in every view because the color depends on its position in the team list.
const palette = [
  '#ef4444', // red
  '#3b82f6', // blue
  '#22c55e', // green
  '#f59e0b', // amber
  '#a855f7', // purple
  '#ec4899', // pink
  '#14b8a6', // teal
  '#f97316', // orange
]

export const teamColor = (teams, teamId) => {
  const index = teams.findIndex((team) => team.id == teamId)
  return palette[(index < 0 ? 0 : index) % palette.length]
}
