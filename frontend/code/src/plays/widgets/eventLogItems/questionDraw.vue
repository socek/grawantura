<script setup>
  import { computed, onMounted, ref } from 'vue'
  import { useHostQuestionStore } from "@/plays/hoststore"
  import useQuestionStore from '@/questions/store'
  import deleteEvent from '@/plays/widgets/eventLogItems/deleteEvent.vue'

  const props = defineProps(['playId', 'event'])
  const hostStore = useHostQuestionStore(props.playId)()
  let questionStore = null
  const question = ref(null)

  onMounted(async () => {
    await hostStore.fetch()
    questionStore = useQuestionStore(hostStore.gameId)()
    await questionStore.fetch()
    question.value = questionStore.getItemById(props.event["question_id"])
  })

  const questionText = computed(() => {
    if(!question.value) {
      return ""
    }
    return question.value["question"]
  })
</script>

<template>
  <VaListItem class="list__item">
    <div class="row outline">
      <div class="">
        <div class="item" style="font-weight: bold">
          Wylosowano Pytanie <deleteEvent :eventId="props.event['id']" :playId="props.playId" />
        </div>
        <div class="item question">
          {{ questionText }}
        </div>
      </div>
    </div>
  </VaListItem>
</template>

<style scoped>
  .question {
    font-weight: normal;
    background-color: #eeeeee;
  }
</style>
