<script setup>
  import { onMounted, ref } from 'vue'

  import useTeamStore from '@/teams/store'
  import deleteEvent from '@/plays/widgets/eventLogItems/deleteEvent.vue'

  const props = defineProps(['playId', 'event'])
  const teamStore = useTeamStore(props.playId)()
  const money = ref({})
  const change = ref({})

  onMounted(async () => {
    await teamStore.fetch()
    money.value = {}
    change.value = props.event["payload"]["change"]

    for(const [teamId, value] of Object.entries(props.event["payload"]["money"])) {
      if(value != 0) {
        money.value[teamId] = value
      }
    }

    for(const [teamId, value] of Object.entries(props.event["payload"]["change"])) {
      money.value[teamId] = money.value[teamId] || 0
    }
  })

  const teamName = (teamId) => {
    const team = teamStore.getItemById(teamId)
    if(!team) {
      return ""
    } else {
      return team["name"]
    }
  }

  const getChangeClasses = (teamId) => {
    if(props.event["payload"]["change"][teamId] > 0) {
      return {"bought": true}
    } else if(props.event["payload"]["change"][teamId] < 0) {
      return {"used": true}
    }
    return {}
  }

</script>

<template>
  <VaListItem class="list__item">
    <div class="row outline">
        <div class="hint">
          Podpowiedź <deleteEvent :playId="props.event['id']" />
        </div>
        <div v-for="(value, teamId) in money" :key="teamId" class="smallrow" :class="getChangeClasses(teamId)">
          {{ teamName(teamId) }}: {{ value }}
      </div>
    </div>
  </VaListItem>
</template>

<style scoped>
  .hint {
    font-weight: bold;
  }
  .bought {
    font-weight: bold;
    color: rgb(255, 255, 255);
    background-color: #228200;
    font-size: 12px;
  }
  .used {
    font-weight: bold;
    color: rgb(38, 40, 36);
    background: #FFD43A;
    font-size: 12px;
  }
</style>
