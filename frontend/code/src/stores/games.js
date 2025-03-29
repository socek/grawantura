import axios from 'axios';
import { createDefaultState } from './supabase'

export default createDefaultState("games", async () => {
  return await axios("/api/games")
})
