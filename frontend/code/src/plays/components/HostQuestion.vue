<script setup>
  import { computed, onMounted, ref } from 'vue'
  import { Status } from '@/base/basestore'
  import useHostStore from "@/plays/hoststore"
  const props = defineProps(['playId'])
  const hostStore = useHostStore(props.playId)()

  onMounted(async () => {
    await hostStore.fetchQuestion()
  })

  const isLoading = computed(() => {
    return [Status.BeforeLoad, Status.Loading].indexOf(hostStore.questionStatus) != -1
  })
</script>

<template>
  <VaCard v-if="!isLoading && hostStore.question">
    <VaCardTitle>Pytanie</VaCardTitle>
    <VaCardActions align="stretch">
      <VaButton color="success">Dobra Odpowiedź</VaButton>
      <VaButton color="danger">Zła Odpowiedź</VaButton>
      <VaButton color="warning">Pokaż podpowiedź</VaButton>
    </VaCardActions>
    <VaCardContent>
      <div class="">
        <span class="bold">Pytanie:</span>{{ hostStore.question.question }}
      </div>
      <div class="">
        <span class="bold">Odpowiedź:</span>{{ hostStore.question.answer }}
      </div>
      <div class="text-block">
        <p class="bold">Podpowiedzi:</p>
        <textarea readonly>{{ hostStore.question.hints }}</textarea>
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
  <VaCard v-if="!isLoading && hostStore.question == null">
    <VaCardTitle>Pytanie</VaCardTitle>
    <VaAlert color="warning" class="mb-6">
      Nie wylosowano pytania!
    </VaAlert>
    <VaCardActions align="stretch">
      <VaButton disabled="true" color="success">Dobra Odpowiedź</VaButton>
      <VaButton disabled="true" color="danger">Zła Odpowiedź</VaButton>
      <VaButton disabled="true" color="warning">Pokaż podpowiedź</VaButton>
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
