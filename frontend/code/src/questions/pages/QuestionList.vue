<script setup>
  import { ref } from 'vue'
  import { useRoute } from 'vue-router'
  import ItemTable from '@/questions/components/QuestionTable.vue'
  import createQuestionForm from '@/questions/widgets/createQuestion.vue'

  const route = useRoute()
  const questionFilter = ref("")
</script>

<template>
  <div>
    <h1 class="page-title font-bold">Questions</h1>
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
          <createQuestionForm :gameId="route.params.gameId" />
        </div>

        <ItemTable class="w-full md:w-1/2" :gameId="route.params.gameId" :questionFilter="questionFilter" />
      </VaCardContent>
    </VaCard>
  </div>
</template>
