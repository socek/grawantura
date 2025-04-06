<script setup>
  import GamesTable from '@/games/components/GamesTable.vue'
  import { ref } from 'vue'
  import createGameForm from '@/games/widgets/createGame.vue'

  const nameFilter = ref("")
</script>

<template>
  <div>
    <h1 class="page-title font-bold">Games</h1>
    <VaCard>
      <VaCardContent>
        <div class="flex flex-col md:flex-row gap-2 mb-2 justify-between">
          <div class="flex flex-col md:flex-row gap-2 justify-start">
            <VaInput v-model="nameFilter" placeholder="Search">
              <template #prependInner>
                <VaIcon name="search" color="secondary" size="small" />
              </template>
            </VaInput>
          </div>
          <createGameForm  ref="createGameFormRef" />
        </div>

        <GamesTable class="w-full md:w-1/2" :nameFilter="nameFilter" />
      </VaCardContent>
    </VaCard>
  </div>
</template>
