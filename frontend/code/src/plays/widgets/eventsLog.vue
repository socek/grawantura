<script setup>
  import { computed, onMounted, ref } from 'vue'
  import { Status } from '@/base/basestore'
  import { useHostQuestionStore } from "@/plays/hoststore"
  import useTeamStore from '@/teams/store'
  import QuestionDraw from '@/plays/widgets/eventLogItems/questionDraw.vue'
  import EndAuction from '@/plays/widgets/eventLogItems/endAuction.vue'
  import InitMoney from '@/plays/widgets/eventLogItems/initMoney.vue'
  import Hint from '@/plays/widgets/eventLogItems/hint.vue'
  import Answer from '@/plays/widgets/eventLogItems/answer.vue'

  const props = defineProps(['playId'])
  const questionStore = useHostQuestionStore(props.playId)()
  const teamStore = useTeamStore(props.playId)()

  onMounted(async () => {
    await questionStore.fetch()
    await teamStore.fetch()
  })

  const isLoading = computed(() => {
    return [Status.BeforeLoad, Status.Loading].indexOf(questionStore.questionStatus) != -1
  })

  const isGoup = (event) => {
    return ['answer', 'end auction'].includes(event['typename'])
  }

</script>

<template>
  <VaCard class="p-3 eventlogmain">
    <VaCardTitle>Historia</VaCardTitle>
    <VaCardContent class="h-[30vh] w-full overflow-auto scrollbarbottom eventlog">
      <VaList>
        <div
          class="flex flex-col md6 bigrow"
          v-for="event in questionStore.events"
          :class="{ goupelo: isGoup(event) }"
          :key="event['id']">
            <QuestionDraw :playId="props.playId" :key="event['id']" :event="event" v-if="event['typename'] == 'question draw'" />
            <EndAuction :playId="props.playId" :key="event['id']" :event="event" v-if="event['typename'] == 'end auction'" />
            <InitMoney :playId="props.playId" :key="event['id']" :event="event" v-if="event['typename'] == 'init money'" />
            <Hint :playId="props.playId" :key="event['id']" :event="event" v-if="event['typename'] == 'hint'" />
            <Answer :playId="props.playId" :key="event['id']" :event="event" v-if="event['typename'] == 'answer'" />
        </div>
        <hr class="hrend" />
      </VaList>
    </VaCardContent>
  </VaCard>
</template>

<style>
  .item {
    text-align: center;
  }
  .row {
    width: 100%;
  }
  .smallrow {
    float: left;
    padding: 0 15px;
    border: #000000 solid 1px;
    width: 150px;
  }
  .list__item {
    margin: 10px 0;
  }
  .scrollbarbottom {
    overflow: auto;
    display: flex;
    flex-direction: column-reverse;
  }
  .goupelo {
    margin-top: -17px;

  }
  .bigrow {
    width: 450px;
  }
  .eventlog {
    min-height: 400px;
  }
  .hrend {
    border-color: red;
  }
</style>
