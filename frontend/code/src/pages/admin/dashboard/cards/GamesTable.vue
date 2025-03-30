<script setup>
import { onMounted, ref, computed } from 'vue'
import { defineVaDataTableColumns } from 'vuestic-ui'

import { Status } from '@/base/basestore'
import useGamesStore from '@/pages/admin/games/store'
const gamesStore = useGamesStore()

onMounted(async () => {
  await gamesStore.fetch()
})

const isLoading = computed(() => {
  return [Status.BeforeLoad, Status.Loading].indexOf(gamesStore.getStatus) != -1
})

const columns = defineVaDataTableColumns([
  { label: 'Name', key: 'name', sortable: true },
])
</script>

<template>
  <VaCard>
    <VaCardTitle class="flex items-start justify-between">
      <h1 class="card-title text-secondary font-bold uppercase">Games</h1>
      <VaButton preset="primary" size="small" to="/games">View all games</VaButton>
    </VaCardTitle>
    <VaCardContent>
      <div v-if="gamesStore.items.length > 0">
        <VaDataTable
          :items="gamesStore.items"
          :columns="columns"
          :loading="isLoading"
        >
         ` <template #cell(name)="{ rowData }">
            <div class="ellipsis max-w-[230px] lg:max-w-[450px]">
              {{ rowData.name }}
            </div>
          </template>
        </VaDataTable>
      </div>
      <div v-else class="p-4 flex justify-center items-center text-[var(--va-secondary)]">No games</div>
    </VaCardContent>
  </VaCard>
</template>
