<script setup>
  import { supabase } from '../supabase'
  import { onMounted, ref, toRefs } from 'vue'

  const props = defineProps(['session'])
  const { session } = toRefs(props)

  const loading = ref(true)
  const games = ref()

  onMounted(() => {
    getGames()
  })

  async function getGames() {
    try {
      loading.value = true

      const { data, error, status } = await supabase
        .from('games')
        .select(`*`)

      if (error && status !== 406) throw error

      if (data) {
        games.value = data
      }
    } catch (error) {
      console.log(error.message)
    } finally {
      loading.value = false
    }
  }

  function getUrl(game) {
    return "/game/" + game.id
  }
</script>

<template>
  <p>Hello, this is VUE.</p>
  <p v-if="loading">Loading...</p>
  <ul>
    <li v-for="game in games">
      <RouterLink :to="getUrl(game)">{{game.name}}</RouterLink>
    </li>
  </ul>
</template>
