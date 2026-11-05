<script setup>
  import { onMounted } from 'vue'
  import { useRoute } from 'vue-router'

  import { useHostViewStore } from "@/plays/hoststore"

  import QuestionModal from '@/plays/pages/pages/question.vue'
  import TimetableModal from '@/plays/pages/pages/timetable.vue'
  import ScoreboardModal from '@/plays/pages/pages/scoreboard.vue'

  const route = useRoute()
  const viewStore = useHostViewStore(route.params.playId)()

  onMounted(async () => {
    await viewStore.fetch()
  })

</script>

<template>
  <div class="h-full w-full">
    <QuestionModal
      v-if="viewStore.payload.name == 'question'"
      :playId="route.params.playId"
    />
    <TimetableModal
      v-else-if="viewStore.payload.name == 'timetable'"
      :playId="route.params.playId"
    />
    <ScoreboardModal
      v-else-if="viewStore.payload.name == 'scoreboard'"
      :playId="route.params.playId"
    />
    <div v-else class="h-full w-full flex items-center justify-center">
      <h1 class="logo">Grawantura</h1>
    </div>
  </div>
</template>

<style scoped>
  .logo {
    font-size: clamp(3rem, 10vw, 9rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(90deg, #f472b6, #facc15, #38bdf8);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }
</style>
