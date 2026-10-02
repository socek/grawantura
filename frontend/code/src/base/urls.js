export const gamesUrl = () => "/api/games"
export const questionsUrl = (gameId) => `/api/games/${gameId}/questions`
export const playsUrl = (gameId) => `/api/games/${gameId}/plays`
export const teamsUrl = (playId) => `/api/plays/${playId}/teams`
export const hostUrl = (playId, command) => `/api/host/${playId}/${command}`
export const timerUrl = (playId, command) => {
  let ending = ''
  if(command) {
    ending = `/${command}`
  }
  return `/api/timer/${playId}${ending}`
}
