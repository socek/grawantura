<script setup>
  import { ref, onMounted } from 'vue'

  import useTeamStore from '@/teams/store'
  import deleteEvent from '@/plays/widgets/eventLogItems/deleteEvent.vue'

  const props = defineProps(['playId', 'event'])
  const teamStore = useTeamStore(props.playId)()

  onMounted(async () => {
    await teamStore.fetch()
  })

  const payload = ref(props.event["payload"])
  const teamName = (teamId) => {
    const team = teamStore.getItemById(teamId)
    if(team) {
      return team["name"]
    }
    return ""
  }
</script>

<template>
  <VaListItem class="list__item">
    <div class="row outline">
      <div class="">
        <div class="item" style="font-weight: bold">
          Początek Gry <deleteEvent :eventId="props.event['id']" :playId="props.playId" />
        </div>
        <div class="smallrow" v-for="(value, teamId) in payload" :key="teamId">
          {{ teamName(teamId) }}: {{ value }}
        </div>
      </div>
    </div>
  </VaListItem>
</template>

<style>
  .item {
    text-align: center;
  }
  .smallrow {
    float: left;
    padding: 0 15px;
    border: blue solid 1px;
  }
</style>
