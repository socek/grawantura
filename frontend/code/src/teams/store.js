import { ref, computed } from 'vue'
import { defineStore } from "pinia"
import { Status, sleep } from '@/base/basestore'
import { teamsUrl } from '@/base/urls'

import jwtCall from "@/auth/calls"

export default (playId) => defineStore("teams_" + playId, () => {
  const items = ref([])
  const status = ref(Status.BeforeLoad)

  function getItemById(itemId) {
    if (status.value != Status.Completed) {
      return null
    }
    for (const item of items.value) {
      if(item["id"] == itemId) {
        return item
      }
    }
    return null
  }

  async function fetch(force) {
    force = force || false
    if (!force && status.value != Status.BeforeLoad) {
      while(status.value != Status.Completed) {
        await sleep(300)
      }
      return
    }
    status.value = Status.Loading
    try {
      const { data, error, reqstatus } = await jwtCall({
        url: teamsUrl(playId),
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
    getItemById,
  }
})
