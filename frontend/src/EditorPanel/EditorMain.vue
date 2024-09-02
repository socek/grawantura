<script setup>
  import { onMounted, ref, computed } from 'vue'
  import { useStore } from 'vuex'
  import { Status } from '@/models/consts'
  import { supabase } from '@/models/supabase'
  import CreateGame from './widgets/CreateGame.vue'

  const store = useStore()

  const isLoaded = computed(() => {
    return store.getters["games/getStatus"] == Status.Completed
  })
  const games = computed(() => {
    return store.getters["games/getItems"]
  })

  onMounted(async () => {
    store.dispatch("games/fetch")
  })
</script>

<template>
  <div>
    <h1>Panel Edytora</h1>
    <CreateGame />
    <ul v-if="isLoaded">
      <li v-for="game in games" :key="game.id">{{ game.name }}</li>
    </ul>
    <div v-else>
      Loading...
    </div>
  </div>
</template>

