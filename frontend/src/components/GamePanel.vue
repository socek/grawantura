<script setup>
  import { supabase } from '../models/supabase'
  import { onMounted, ref } from 'vue'
  import { useRoute } from 'vue-router'
  const route = useRoute()

  const loading = ref(false)
  const questions = ref()
  const lastMsg = ref()

  onMounted(async () => {
    loading.value = true
    questions.value = await fetchQuestions()
    loading.value = false
  })

  const handleInserts = async (payload) => {
    // loading.value = true
    // questions.value = await fetchQuestions()
    // loading.value = false
    console.log("onChange", payload)
    if (payload.payload.gameId == route.params.gameId) {
      lastMsg.value = payload.payload.message
    }
  }

  // Listen to inserts
  supabase
    .channel('commands')
    .on('broadcast', { event: 'test-my-messages' }, handleInserts)
    .subscribe()

  async function fetchQuestions() {
    try {
      const { data, error, status } = await supabase
        .from('questions')
        .select(`*`)
        .eq('game_id', route.params.gameId)

      if (error && status !== 406) throw error

      if (data) {
        return data
      }
    } catch (error) {
      console.log(error.message)
    }
  }

async function elo () {
  console.log("sending")
  console.log(await supabase
    .channel('commands')
    .send({
        type: 'broadcast',
        event: 'test-my-messages',
        payload: { message: 'talking to myself', gameId: route.params.gameId },
      }))
}
</script>

<template>
  <p v-if="loading">Loading...</p>
  <ul>
    <li @click="elo()" v-for="question in questions">
      {{question.question}}
    </li>
  </ul>

  <div>
    {{ lastMsg }}
  </div>

</template>
