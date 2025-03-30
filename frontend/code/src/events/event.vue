<script setup>
  import { onMounted, onUnmounted, ref } from 'vue'
  import jwtCall from "@/auth/calls"
  import useAuthStore from "@/auth/store"

  const EVENTS_URL = "/api/events"
  let lastTime = null;
  let cycleReference = null;
  const authStore = useAuthStore()

  const fetchData = async () => {
    if (!authStore.isAuthorized) {
      lastTime = null;
      return
    }
    const res = await jwtCall({
      "url": EVENTS_URL,
      "method": "GET",
      "data": {
          params: {"time": lastTime}
      }
    })
    res.data.elements.forEach(async (element) => {
      console.log("event", element) // TODO: do something with the data
    })
    lastTime = res.data.time
  }

  onMounted(async () => {
    cycleReference = setInterval(fetchData, 1000)
  })

  onUnmounted(async () => {
    clearInterval(cycleReference)
  })
</script>

<template>
</template>
