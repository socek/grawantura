<script setup>
  import { computed, onMounted } from 'vue'

  import useTeamStore from '@/teams/store'
  import { useHostQuestionStore } from "@/plays/hoststore"
  import deleteEvent from '@/plays/widgets/eventLogItems/deleteEvent.vue'

  const props = defineProps(['playId', 'event'])
  const teamStore = useTeamStore(props.playId)()
  const questionStore = useHostQuestionStore(props.playId)()

  onMounted(async () => {
    await teamStore.fetch()
    await questionStore.fetch()
  })

  const teamAuctioned = computed(() => {
    const payload = {}
    for (const [key, value] of Object.entries(props.event["payload"])) {
      if(key == "addon") {
        continue
      }
      payload[key] = value
    }
    return payload
  })
  const addonMoney = computed(() => {
    return props.event["payload"]["addon"]
  })

  const moneyPool = computed(() => {
    return props.event["money_stamp"]
  })

  const sumMoney = computed(() => {
    let result = props.event["money_stamp"]
    for (const [key, value] of Object.entries(props.event["payload"])) {
      result += value
    }
    return result
  })

  const teamName = (teamId) => {
    const team = teamStore.getItemById(teamId)
    if(team) {
      return team["name"]
    }
    return ""
  }
  const hasWon = (matchTeamId) => {
    let teamId = null
    let greatesValue = 0
    for (const [key, value] of Object.entries(props.event["payload"])) {
      if(value > greatesValue) {
        greatesValue = value
        teamId = key
      }
    }
    return teamId == matchTeamId
  }
</script>

<template>
  <VaListItem class="list__item">
    <div class="row outline">
      <div class="item myitem">
        Licytacja <deleteEvent :eventId="props.event['id']" :playId="props.playId" />
      </div>
      <div class="smallrow noteam">
        Pula Przed: {{ moneyPool }}
      </div>
      <div class="smallrow noteam">
        Dodatek: {{ addonMoney }}
      </div>
      <div class="smallrow noteam">
        Suma: {{ sumMoney }}
      </div>
      <div v-for="(value, teamId) in teamAuctioned" :key="teamId" class="smallrow" :class="{'win': hasWon(teamId)}">
        {{ teamName(teamId) }}: {{ value }}
      </div>
    </div>
  </VaListItem>
</template>

<style scoped>
  .myitem {
    font-weight: bold;
  }
  .win {
    font-weight: bold;
    color: rgb(255, 255, 255);
    background-color: #228200;
  }
  .noteam {
    background-color: #222222;
    color: #eeeeee;
  }
</style>
