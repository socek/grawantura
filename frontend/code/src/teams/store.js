import { ref, computed } from 'vue'
import { defineStore } from "pinia"
import { Status } from '@/base/basestore'
import { teamsUrl } from '@/base/urls'

import jwtCall from "@/auth/calls"

export default (playId) => defineStore("teams_" + playId, () => {
  const items = ref([])
  const status = ref(Status.BeforeLoad)

  function getItemById(itemId) {
    if (status.value != Status.Completed) {
      return ""
    }
    for (const item of items.value) {
      if(item["id"] == itemId) {
        return item
      }
    }
  }

  async function fetch(force) {
    force = force || false
    if (!force && status.value == Status.Completed) {
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
