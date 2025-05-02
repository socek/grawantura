<script setup>
  import { computed } from 'vue'
  import { useRoute } from 'vue-router'
  import TeamTable from "@/teams/components/TeamTable.vue"
  import createTeamForm from "@/teams/widgets/createTeam.vue"
  import playAdmin from "@/plays/components/PlayAdmin.vue"
  import HostQuestion from "@/plays/components/HostQuestion.vue"
  import HostTimer from "@/plays/components/HostTimer.vue"

  const route = useRoute()
  const playId = computed(() => route.params.playId)
</script>

<template>
  <div class="flex flex-wrap gap-5">
    <VaCard class="" horizontal>
      <div class="flex-auto">
        <VaCardTitle>Drużyny</VaCardTitle>
        <VaCardContent>
          <div class="flex flex-col md:flex-row gap-2 mb-2 justify-between">
            <createTeamForm :playId="playId" :key="playId" />
          </div>
          <div class="flex flex-col md:flex-row gap-2 mb-2 justify-between">
            <TeamTable :playId="playId" />
          </div>
        </VaCardContent>
      </div>
    </VaCard>
    <playAdmin :playId="playId" />
    <HostTimer :playId="playId" />
    <HostQuestion :playId="playId" />
  </div>
</template>

