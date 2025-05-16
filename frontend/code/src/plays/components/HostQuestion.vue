<script setup>
  import { computed, onMounted, ref } from 'vue'
  import { Status } from '@/base/basestore'
  import { useHostQuestionStore } from "@/plays/hoststore"
  import useTeamStore from '@/teams/store'
  import commands from "@/plays/commands"

  const props = defineProps(['playId'])
  const teamStore = useTeamStore(props.playId)()
  const questionStore = useHostQuestionStore(props.playId)()

  onMounted(async () => {
    await questionStore.fetch()
    await teamStore.fetch()
  })

  const isLoading = computed(() => {
    return [Status.BeforeLoad, Status.Loading].indexOf(questionStore.questionStatus) != -1
  })

  const successAnswer = async () => {
    await commands.answer(props.playId, true)
  }

  const failedAnswer = async () => {
    await commands.answer(props.playId, false)
  }

  const showHints = async () => {
    await commands.useHint(props.playId, questionStore.answeringTeamId)
  }

  const isDisabled = computed(() => {
    return questionStore.answeringTeamId === null
  })

  const isHintDisabled = computed(() => {
    return questionStore.showHint || questionStore.answeringTeamId === null
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
    <VaCardTitle>Pytanie</VaCardTitle>
    <VaCardActions align="stretch">
      <VaButton
        :disabled="isDisabled"
        color="success"
        @click="successAnswer">
          Dobra Odpowiedź
      </VaButton>
      <VaButton
        :disabled="isDisabled"
        color="danger"
        @click="failedAnswer">
          Zła Odpowiedź
      </VaButton>
      <VaButton
        :disabled="isHintDisabled"
        color="warning"
        @click="showHints">
          Pokaż podpowiedź
      </VaButton>
    </VaCardActions>
    <VaCardContent>
      <div class="">
        <span class="bold">Odpowiada:</span> {{ teamName }}
      </div>
      <div class="">
        <span class="bold">Pytanie:</span> {{ questionStore.question.question }}
      </div>
      <div class="">
        <span class="bold">Odpowiedź:</span> {{ questionStore.question.answer }}
      </div>
      <div class="text-block">
        <p class="bold">Podpowiedzi:</p>
        <textarea readonly>{{ questionStore.question.hints }}</textarea>
      </div>
    </VaCardContent>
  </VaCard>
  <VaInnerLoading v-if="isLoading" loading>
    <VaCard>
      <VaCardTitle>Pytanie</VaCardTitle>
      <VaCardActions align="stretch">
        <VaButton color="success">Dobra Odpowiedź</VaButton>
        <VaButton color="danger">Zła Odpowiedź</VaButton>
        <VaButton color="warning">Pokaż podpowiedź</VaButton>
      </VaCardActions>
      <VaCardContent>
        <div class="">
          <span class="bold">Pytanie:</span>
        </div>
        <div class="">
          <span class="bold">Odpowiedź:</span>
        </div>
        <div class="text-block">
          <p class="bold">Podpowiedzi:</p>
          <textarea readonly></textarea>
        </div>
      </VaCardContent>
    </VaCard>
  </VaInnerLoading>
  <VaCard v-if="!isLoading && questionStore.question == null">
    <VaCardTitle>Pytanie</VaCardTitle>
    <VaAlert color="warning" class="mb-6">
      Nie wylosowano pytania!
    </VaAlert>
    <VaCardActions align="stretch">
      <VaButton :disabled="true" color="success">Dobra Odpowiedź</VaButton>
      <VaButton :disabled="true" color="danger">Zła Odpowiedź</VaButton>
      <VaButton :disabled="true" color="warning">Pokaż podpowiedź</VaButton>
    </VaCardActions>
    <VaCardContent>
      <div class="">
        <span class="bold">Pytanie:</span>
      </div>
      <div class="">
        <span class="bold">Odpowiedź:</span>
      </div>
      <div class="text-block">
        <p class="bold">Podpowiedzi:</p>
        <textarea readonly></textarea>
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
