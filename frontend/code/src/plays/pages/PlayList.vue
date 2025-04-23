<script setup>
  import { ref, computed, watch } from 'vue'
  import { useRoute } from 'vue-router'
  import gameSelect from '@/questions/widgets/gameSelect.vue'
  import ItemTable from '@/plays/components/PlayTable.vue'
  import createPlayForm from '@/plays/widgets/createPlay.vue'

  const route = useRoute()
  const playFilter = ref("")
  const gameId = computed(() => route.params.gameId)
  watch(gameId, () => {
    playFilter.value = ""
  })
</script>

<template>
  <div>
    <h1 class="page-title font-bold">Plays</h1>
    <VaCard>
      <VaCardContent>
        <div class="flex flex-col md:flex-row gap-2 mb-2 justify-between">
          <div class="flex flex-col md:flex-row gap-2 justify-start">
            <gameSelect :gameId="gameId" routeName="plays" />
          </div>
        </div>
      </VaCardContent>
    </VaCard>
    <div id="barpause">&nbsp;</div>
    <VaCard>
      <VaCardContent>
        <div class="flex flex-col md:flex-row gap-2 mb-2 justify-between">
          <div class="flex flex-col md:flex-row gap-2 justify-start">
            <VaInput v-model="playFilter" placeholder="Search">
              <template #prependInner>
                <VaIcon name="search" color="secondary" size="small" />
              </template>
            </VaInput>
          </div>
          <createPlayForm :gameId="gameId" :key="gameId" />
        </div>

        <ItemTable class="w-full md:w-1/2" :gameId="gameId" :key="gameId" :playFilter="playFilter" />
      </VaCardContent>
    </VaCard>
  </div>
</template>

<style scoped>
  #barpause {
    height: 10px;
  }
</style>
