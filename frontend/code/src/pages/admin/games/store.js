
import { createDefaultState } from '@/base/basestore.js'
import useGamesStore from './store'
import useAuthStore from "@/auth/store"

import jwtCall from "@/auth/calls"

export default createDefaultState("games", async () => {
  return await jwtCall({
    url: "/api/games",
    method: "get",
  })
})
