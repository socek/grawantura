<script setup>
  import { onMounted, onUnmounted } from 'vue'
  import useAuthStore from "@/auth/store"
  import useGamesStore from '@/games/store'
  import useQuestionStore from '@/questions/store'
  import usePlayStore from '@/plays/store'
  import useTeamStore from '@/teams/store'

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
      } else if(payload["payload"]["group"] == "questions") {
        const gameId = payload["payload"]["game_id"]
        await useQuestionStore(gameId)().fetch(true)
      } else if(payload["payload"]["group"] == "plays") {
        const gameId = payload["payload"]["game_id"]
        await usePlayStore(gameId)().fetch(true)
      } else if(payload["payload"]["group"] == "teams") {
        const playId = payload["payload"]["play_id"]
        await useTeamStore(playId)().fetch(true)
      } else {
        console.log("Unknow refresh", payload);
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
