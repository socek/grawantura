<script setup>
  import { ref, computed, watch } from 'vue'
  import { useRoute } from 'vue-router'
  import ItemTable from '@/questions/components/QuestionTable.vue'
  import createQuestionForm from '@/questions/widgets/createQuestion.vue'
  import gameSelect from '@/questions/widgets/gameSelect.vue'

  const route = useRoute()
  const questionFilter = ref("")
  const gameId = computed(() => route.params.gameId)
  watch(gameId, () => {
    questionFilter.value = ""
  })
</script>

<template>
  <div>
    <h1 class="page-title font-bold">Questions</h1>
    <VaCard>
      <VaCardContent>
        <div class="flex flex-col md:flex-row gap-2 mb-2 justify-between">
          <div class="flex flex-col md:flex-row gap-2 justify-start">
            <gameSelect :gameId="gameId" />
          </div>
        </div>
      </VaCardContent>
    </VaCard>
    <div id="barpause">&nbsp;</div>
    <VaCard>
      <VaCardContent>
        <div class="flex flex-col md:flex-row gap-2 mb-2 justify-between">
          <div class="flex flex-col md:flex-row gap-2 justify-start">
            <VaInput v-model="questionFilter" placeholder="Search">
              <template #prependInner>
                <VaIcon name="search" color="secondary" size="small" />
              </template>
            </VaInput>
          </div>
          <createQuestionForm :gameId="gameId" :key="gameId" />
        </div>

        <ItemTable class="w-full md:w-1/2" :gameId="gameId" :key="gameId" :questionFilter="questionFilter" />
      </VaCardContent>
    </VaCard>
  </div>
</template>

<style scoped>
  #barpause {
    height: 10px;
  }
</style>
