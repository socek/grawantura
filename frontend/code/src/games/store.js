import { createDefaultState } from '@/base/basestore.js'
import { gamesUrl } from '@/base/urls'
import jwtCall from "@/auth/calls"

export default createDefaultState("games", async () => {
  return await jwtCall({
    url: gamesUrl(),
    method: "get",
  })
})
