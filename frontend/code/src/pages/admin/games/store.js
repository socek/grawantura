import axios from 'axios';
import { createDefaultState } from '@/base/basestore.js'

export default createDefaultState("games", async () => {
  return await axios("/api/games")
})
