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
      v-if="viewStore.payload.name == 'timetable'"
      :playId="route.params.playId"
    />
    <ScoreboardModal
      v-if="viewStore.payload.name == 'scoreboard'"
      :playId="route.params.playId"
    />
  </div>
</template>
