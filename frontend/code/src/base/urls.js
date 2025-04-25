export const gamesUrl = () => "/api/games"
export const questionsUrl = (gameId) => `/api/games/${gameId}/questions`
export const playsUrl = (gameId) => `/api/games/${gameId}/plays`
export const teamsUrl = (playId) => `/api/plays/${playId}/teams`
