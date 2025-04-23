import { ref, computed } from 'vue'
import { defineStore } from "pinia"
import { Status } from '@/base/basestore'
import { playsUrl } from '@/base/urls'

import jwtCall from "@/auth/calls"

export default (gameId) => defineStore("plays_" + gameId, () => {
  const items = ref([])
  const status = ref(Status.BeforeLoad)

  async function fetch(force) {
    force = force || false
    if (!force && status.value == Status.Completed) {
      return
    }
    status.value = Status.Loading
    try {
      const { data, error, reqstatus } = await jwtCall({
        url: playsUrl(gameId),
        method: "get",
      })

      if (error && reqstatus !== 406) throw error
      if (data) {
        items.value = data.items
        status.value = Status.Completed
      } else {
        status.value = Status.Failed
      }
    } catch (error) {
      status.value = Status.Failed
    }
  }
  return {
    items,
    status,
    fetch,
  }
})
