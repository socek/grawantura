<script setup>
  import QuestionsTable from '@/pages/admin/questions/components/QuestionsTable.vue'
  import { ref } from 'vue'
  import createQuestionForm from '@/pages/admin/questions/widgets/createQuestion.vue'

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
          <createQuestionForm />
        </div>

        <QuestionsTable class="w-full md:w-1/2" :questionFilter="questionFilter" />
      </VaCardContent>
    </VaCard>
  </div>
</template>
