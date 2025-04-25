<script setup>
import { computed, onMounted, ref } from 'vue'

import { Status } from '@/base/basestore'
import useTeamStore from '@/teams/store.js'

import editTeamForm from '@/teams/widgets/editTeam.vue'
import deleteTeamForm from '@/teams/widgets/deleteTeam.vue'

const props = defineProps(['playId'])
const teamStore = useTeamStore(props.playId)()

onMounted(async () => await teamStore.fetch())

const isLoading = computed(() => [Status.BeforeLoad, Status.Loading].indexOf(teamStore.status) != -1)

const columns = [
  { label: 'Name', key: 'name', sortable: true },
  { label: ' ', key: 'actions', align: 'right' },
]

const perPage = ref(10)
const teams = computed(() => teamStore.items)
const pageNumber = ref(1)
const totalPages = computed(() => 1)

</script>

<template>
  <div>
    <VaDataTable
      :columns="columns"
      :items="teams"
      :loading="isLoading"
    >
      <template #cell(name)="{ rowData }">
        <div class="flex items-center gap-2 max-w-[230px] ellipsis">
          {{ rowData.name }}
        </div>
      </template>

      <template #cell(actions)="{ rowData }">
        <div class="flex gap-2 justify-end">
          <editTeamForm :itemId="rowData.id" :playId="props.playId" />
          <deleteTeamForm :itemId="rowData.id" :playId="props.playId" :name="rowData.name" />
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
