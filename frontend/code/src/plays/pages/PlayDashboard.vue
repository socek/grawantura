<script setup>
  import { computed } from 'vue'
  import { useRoute } from 'vue-router'
  import TeamTable from "@/teams/components/TeamTable.vue"
  import createTeamForm from '@/teams/widgets/createTeam.vue'

  const route = useRoute()
  const playId = computed(() => route.params.playId)
</script>

<template>
  <div>
    <h1 class="page-title font-bold">Play Dashboard</h1>
    <VaCard>
      <VaCardContent>
        <div class="flex flex-col md:flex-row gap-2 mb-2 justify-between">
          <createTeamForm :playId="playId" :key="playId" />
        </div>
        <div class="flex flex-col md:flex-row gap-2 mb-2 justify-between">
          <TeamTable :playId="playId" />
        </div>

      </VaCardContent>
    </VaCard>
  </div>
</template>

<style scoped>
  #barpause {
    height: 10px;
  }
</style>
