<script setup>
  import { onMounted, onUnmounted } from 'vue'
  import useAuthStore from "@/auth/store"
  import useGamesStore from '@/pages/admin/games/store'

  const gamesStore = useGamesStore()

  const EVENTS_URL = "/api/ws"
  const authStore = useAuthStore()
  let socket = null;

  const eventHandlers = {
    handshake: async (socket, payload) => {
      const response = {
        type: "handshake",
        token: authStore.getToken,
      }
      socket.send(JSON.stringify(response));
    },
    refresh: async (socket, payload) => {
      if(payload["payload"]["group"] == "games") {
        await gamesStore.fetch(true)
      }
    },
  }

  onMounted(async () => {
    socket = new WebSocket(EVENTS_URL)
    console.log("WS Connected...")
    socket.onmessage = async (event) => {
      const payload = JSON.parse(event.data)
      const handler = await eventHandlers[ payload["payload"]["type"] ]
      if(handler) {
        handler(socket, payload)
      } else {
        console.log("Unrecognized event:", payload)
      }
    };

  })

  onUnmounted(() => {
    socket.close()
  })
</script>

<template>
</template>
