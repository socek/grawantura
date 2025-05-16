<script setup>
  import { onMounted, computed } from 'vue'
  import commands from "@/plays/commands"
  import { useHostViewStore } from "@/plays/hoststore"
  import { Status } from '@/base/basestore'

  const props = defineProps(['playId'])
  const hostViewStore = useHostViewStore(props.playId)()

  const drawQuestion = async () => {
    await commands.drawQuestion(props.playId)
  }

  const showScoreboardView = async () => {
    await hostViewStore.clear()
    await commands.changeView(props.playId, "scoreboard")
  }

  const showQuestionView = async () => {
    await hostViewStore.clear()
    await commands.changeView(props.playId, "question")
  }

  const showTimetableView = async () => {
    await hostViewStore.clear()
    await commands.changeView(props.playId, "timetable")
  }

  const viewName = computed(() => hostViewStore.payload.name)
  const viewStatus = (name) => name == viewName.value
  const isLoading = computed(() => {
    return [Status.BeforeLoad, Status.Loading].indexOf(hostViewStore.status) != -1
  })

  onMounted(async () => {
    await hostViewStore.fetch()
  })

</script>

<template>
  <VaCard>
    <VaCardTitle>Licytacja</VaCardTitle>
    <VaCardActions align="stretch" vertical>
      <VaButton color="success" @click="drawQuestion">Losuj Pytanie</VaButton>
      <VaButton :loading="isLoading" :disabled="viewStatus('scoreboard')" @click="showScoreboardView">Scorboard</VaButton>
      <VaButton :loading="isLoading" :disabled="viewStatus('question')" @click="showQuestionView">Pytanie</VaButton>
      <VaButton :loading="isLoading" :disabled="viewStatus('timetable')" @click="showTimetableView">Timetable</VaButton>
    </VaCardActions>
  </VaCard>
</template>
