<script setup>
  import { onMounted, onUnmounted } from 'vue'
  import useAuthStore from "@/auth/store"
  import useGamesStore from '@/games/store'
  import useQuestionStore from '@/questions/store'
  import usePlayStore from '@/plays/store'
  import useTeamStore from '@/teams/store'
  import { useHostQuestionStore, useHostViewStore } from "@/plays/hoststore"

  const gamesStore = useGamesStore()

  const EVENTS_URL = "/api/ws"
  const authStore = useAuthStore()
  let socket = null;

  const host_action_reload_actions = [
    "draw_question",
    "game start",
    "end auction",
    "hint",
    "answer",
  ]

  const eventHandlers = {
    handshake: async (socket, data) => {
      const response = {
        type: "handshake",
        token: authStore.getToken,
      }
      socket.send(JSON.stringify(response));
    },
    refresh: async (socket, data) => {
      const payload = data["payload"]
      if(payload["group"] == "games") {
        await gamesStore.fetch(true)
      } else if(payload["group"] == "questions") {
        const gameId = payload["game_id"]
        await useQuestionStore(gameId)().fetch(true)
      } else if(payload["group"] == "plays") {
        const gameId = payload["game_id"]
        await usePlayStore(gameId)().fetch(true)
      } else if(payload["group"] == "teams") {
        const playId = payload["play_id"]
        await useTeamStore(playId)().fetch(true)
      } else {
        console.log("Unknow refresh", data);
      }
    },
    host_action: async (socket, data) => {
      const payload = data["payload"]
      if(host_action_reload_actions.includes(payload["name"])) {
        const playId = payload["play_id"]
        await useHostQuestionStore(playId)().fetch(true)
      } else if(payload["name"] == "change_view") {
        const playId = payload["play_id"]
        await useHostViewStore(playId)().fetch(true)
      } else {
        console.log("Unknown host action", data)
      }
    }
  }

  onMounted(async () => {
    socket = new WebSocket(EVENTS_URL)
    console.log("WS Connected...")
    socket.onmessage = async (event) => {
      const data = JSON.parse(event.data)
      const handler = eventHandlers[ data["payload"]["type"] ]
      if(handler) {
        await handler(socket, data)
      } else {
        console.log("Unrecognized event:", data)
      }
    };

  })

  onUnmounted(() => {
    socket.close()
  })
</script>

<template>
</template>
