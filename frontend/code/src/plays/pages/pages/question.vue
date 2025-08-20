<script setup>
  import { computed, onMounted, ref } from 'vue'
  import { Status } from '@/base/basestore'
  import { useHostQuestionStore } from "@/plays/hoststore"
  import useTeamStore from '@/teams/store'
  import commands from "@/plays/commands"

  const props = defineProps(['playId'])
  const teamStore = useTeamStore(props.playId)()
  const questionStore = useHostQuestionStore(props.playId)()

  const isAnswerVisible = computed(() => questionStore.answerStatus > 0)
  const isHintsVisible = computed(() => questionStore.showHint)

  onMounted(async () => {
    await questionStore.fetch()
    await teamStore.fetch()
  })

  const isLoading = computed(() => {
    return [Status.BeforeLoad, Status.Loading].indexOf(questionStore.questionStatus) != -1
  })

  const teamName = computed(() => {
    if (questionStore.answeringTeamId) {
      const team = teamStore.getItemById(questionStore.answeringTeamId)
      return team && team["name"]
    }
    return ""
  })

</script>

<template>
  <VaCard v-if="!isLoading && questionStore.question">
    <VaCardContent>
      <div class="">
        <span class="bold">Odpowiada:</span> {{ teamName }}
      </div>
      <div class="">
        <span class="bold">Pytanie:</span> {{ questionStore.question.question }}
      </div>
      <div class="" v-if="isAnswerVisible">
        <span class="bold">Odpowiedź:</span> {{ questionStore.question.answer }}
      </div>
      <div class="text-block" v-if="isHintsVisible">
        <p class="bold">Podpowiedzi:</p>
        <textarea readonly>{{ questionStore.question.hints }}</textarea>
      </div>
    </VaCardContent>
  </VaCard>
</template>

<style scoped>
  .bold {
    font-size: large;
    font-weight: bold;
  }
  .text-block {
      white-space: pre;
  }
</style>
