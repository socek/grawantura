<script setup>
  import GamesTable from '@/pages/admin/games/components/GamesTable.vue'
  import { ref } from 'vue'
  import createGameForm from '@/pages/admin/games/widgets/createGame.vue'

  const createGameFormRef = ref(null)

  const showAddGame = () => {
    createGameFormRef.value.showDialog()
  }
</script>

<template>
  <h1 class="page-title font-bold">Games</h1>

  <VaCard>
    <VaCardContent>
      <div class="flex flex-col md:flex-row gap-2 mb-2 justify-between">
        <VaButton @click="showAddGame">Add Game</VaButton>
      </div>

      <GamesTable class="w-full md:w-1/2" />
    </VaCardContent>
  </VaCard>

  <createGameForm  ref="createGameFormRef" />
</template>
