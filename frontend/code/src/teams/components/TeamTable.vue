<script setup>
import { computed, onMounted, ref } from 'vue'

import { Status } from '@/base/basestore'
import useTeamStore from '@/teams/store.js'

import editTeamForm from '@/teams/widgets/editTeam.vue'
import deleteTeamForm from '@/teams/widgets/deleteTeam.vue'

const props = defineProps(['playId'])
const teamStore = useTeamStore(props.playId)()


const isLoading = computed(() => [Status.BeforeLoad, Status.Loading].indexOf(teamStore.status) != -1)

const columns = [
  { label: 'Name', key: 'name' },
  { label: 'Posiadane', key: 'money' },
  { label: 'Zalicytowane', key: 'auctioned' },
  { label: 'Dodatek', key: 'addon' },
  { label: ' ', key: 'actions', align: 'right' },
]

const teams = computed(() => teamStore.items)

onMounted(async () => {
  await teamStore.fetch()
})

const adminScoresMoney = ref(0);
const adminScoresAddon = ref(0);
const adminScoresAuctioned = computed(() => {
  let sum = 0
  sum += parseInt(adminScoresMoney.value) || 0
  sum += parseInt(adminScoresAddon.value) || 0
  teamStore.items.forEach((team, index) => {
    sum += parseInt(team.auctioned) || 0
  })
  return sum
});

const isGreatest = (id) => {
  let greatestId = null
  let greatestValue = 0
  teamStore.items.forEach((team, index) => {
    const value = parseInt(team.auctioned) || 0
    if(value > greatestValue) {
      greatestValue = value
      greatestId = team.id
    }
  })
  return greatestId == id
}

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

      <template #cell(money)="{ rowData }">
        <div class="flex gap-2 justify-end">
          <VaInput
            readonly
            v-model="rowData.money"
          />
        </div>
      </template>

      <template #cell(auctioned)="{ rowData }">
        <div class="flex gap-2 justify-end">
          <VaInput
            :success="isGreatest(rowData.id)"
            v-model="rowData.auctioned"
          />
        </div>
      </template>

      <template #cell(addon)="{ rowData }">
        <div class="flex gap-2 justify-end">
          <VaInput
            v-model="rowData.addon"
          />
        </div>
      </template>

      <template #headerPrepend>
        <tr class="table-crud__slot">
          <th class="p-1">
            Pula
          </th>
          <th class="p-1">
            <VaInput
              readonly
              v-model="adminScoresMoney"
            />
          </th>
          <th class="p-1">
            <VaInput
              readonly
              v-model="adminScoresAuctioned"
            />
          </th>
          <th class="p-1">
            <VaInput
              v-model="adminScoresAddon"
            />
          </th>
          <th class="p-1">
            <VaButton block>
              Koniec Licytacji
            </VaButton>
          </th>
        </tr>
      </template>

    </VaDataTable>

  </div>
</template>

<style lang="scss" scoped>
.va-data-table {
  ::v-deep(.va-data-table__table-tr) {
    border-bottom: 1px solid var(--va-background-border);
  }
}
</style>
