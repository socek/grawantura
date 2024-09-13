<script setup>
import { useModal } from 'vuestic-ui'
import { computed, onMounted, ref } from 'vue'
import { useVModel } from '@vueuse/core'

import { Status } from '@/stores/supabase'
import useGamesStore from '@/stores/games'
const gamesStore = useGamesStore()

onMounted(async () => {
  await gamesStore.fetch()
})

const isLoading = computed(() => {
  return [Status.BeforeLoad, Status.Loading].indexOf(gamesStore.getStatus) != -1
})


const columns = [
  { label: 'Full Name', key: 'fullname', sortable: true },
  // { label: 'Email', key: 'email', sortable: true },
  // { label: 'Username', key: 'username', sortable: true },
  // { label: 'Role', key: 'role', sortable: true },
  // { label: 'Projects', key: 'projects', sortable: true },
  // { label: ' ', key: 'actions', align: 'right' },
]

const perPage = ref(10)
const games = computed(() => gamesStore.items)
const pageNumber = ref(1)
const totalPages = computed(() => 1)

</script>

<template>
  <div>
    <VaDataTable
      :columns="columns"
      :items="games"
      :loading="isLoading"
    >
      <template #cell(fullname)="{ rowData }">
        <div class="flex items-center gap-2 max-w-[230px] ellipsis">
          {{ rowData.name }}
        </div>
      </template>

    </VaDataTable>

    <div class="flex flex-col-reverse md:flex-row gap-2 justify-between items-center py-2">
      <div>
        <b>{{ totalPages }} results.</b>
        Results per page
        <VaSelect v-model="perPage" class="!w-20" :options="[10, 50, 100]" />
      </div>

      <div v-if="totalPages > 1" class="flex">
        <VaButton
          preset="secondary"
          icon="va-arrow-left"
          aria-label="Previous page"
          :disabled="pageNumber === 1"
          @click="pageNumber--"
        />
        <VaButton
          class="mr-2"
          preset="secondary"
          icon="va-arrow-right"
          aria-label="Next page"
          :disabled="pageNumber === totalPages"
          @click="pageNumber++"
        />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.va-data-table {
  ::v-deep(.va-data-table__table-tr) {
    border-bottom: 1px solid var(--va-background-border);
  }
}
</style>
