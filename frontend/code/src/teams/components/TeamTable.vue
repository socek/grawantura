<script setup>
import { computed, onMounted, ref } from 'vue'

import { Status } from '@/base/basestore'
import useTeamStore from '@/teams/store'
import { useHostQuestionStore } from "@/plays/hoststore"
import commands from "@/plays/commands"

import editTeamForm from '@/teams/widgets/editTeam.vue'
import deleteTeamForm from '@/teams/widgets/deleteTeam.vue'

const props = defineProps(['playId'])
const questionStore = useHostQuestionStore(props.playId)()
const teamStore = useTeamStore(props.playId)()

const isLoading = computed(() => [Status.BeforeLoad, Status.Loading].indexOf(teamStore.status) != -1)

const columns = [
  { label: 'Name', key: 'name' },
  { label: 'Podpowiedzi', key: 'hinst' },
  { label: 'Posiadane', key: 'money' },
  { label: 'Zalicytowane', key: 'auctioned' },
  { label: 'Dodatek', key: 'addon' },
  { label: ' ', key: 'actions', align: 'right' },
]

const teams = computed(() => teamStore.items)

onMounted(async () => {
  await teamStore.fetch()
  await questionStore.fetch()
})

const adminScoresAddon = ref(0)
const adminScoresAuctioned = computed(() => {
  let sum = 0
  sum += parseInt(adminScoresAddon.value) || 0
  for (const [key, rawValue] of Object.entries(questionStore.auctionedPool)) {
    sum += parseInt(rawValue) || 0
  }
  return sum
});

const isGreatest = (id) => {
  let greatestId = null
  let greatestValue = 0
  for (const [key, rawValue] of Object.entries(questionStore.auctionedPool)) {
    const value = parseInt(rawValue) || 0
    if(value > greatestValue) {
      greatestValue = value
      greatestId = key
    }
  }
  return greatestId == id
}

const getMoney = (team_id) => {
  return questionStore.moneyPool[team_id] || 0
}

const getAuctioned = (team_id) => {
  return questionStore.auctionedPool[team_id] || 0
}

const getAddon = (team_id) => {
  return questionStore.addonPool[team_id] || 0
}

const setAuctioned = (team_id, newValue) => {
  questionStore.auctionedPool[team_id] = parseInt(newValue)
}

const setAddon =  (team_id, newValue) => {
  questionStore.addonPool[team_id] = parseInt(newValue)
}

const endAuction = () => {
  const money = {
    "addon": parseInt(adminScoresAddon.value)
  }
  for (const [key, rawValue] of Object.entries(questionStore.auctionedPool)) {
    if(key == "money_pool") {
      continue
    }
    money[key] = rawValue
  }
  commands.endAuction(props.playId, money)
}

const addHint = (team_id) => {
  const change = {}
  change[team_id] = 1
  const money = {}
  for (const [key, rawValue] of Object.entries(questionStore.addonPool)) {
    if(key == "money_pool") {
      continue
    }
    money[key] = rawValue
  }
  commands.addHint(props.playId, change, money)
}

const getHints = (team_id) => {
  return questionStore.hints[team_id] || 0
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
          <VaButton @click="addHint(rowData.id)" color="warning">
            Podpowiedź
          </VaButton>
        </div>
      </template>

      <template #cell(money)="{ rowData }">
        <div class="flex gap-2 justify-center">
          {{ getMoney(rowData.id) }}
        </div>
      </template>

      <template #cell(auctioned)="{ rowData }">
        <div class="flex gap-2 justify-end">
          <VaInput
            tabindex="2"
            :success="isGreatest(rowData.id)"
            :modelValue="getAuctioned(rowData.id)"
            @update:modelValue="setAuctioned(rowData.id, $event)"
          />
        </div>
      </template>

      <template #cell(addon)="{ rowData }">
        <div class="flex gap-2 justify-end">
          <VaInput
            tabindex="3"
            :modelValue="getAddon(rowData.id)"
            @update:modelValue="setAddon(rowData.id, $event)"
          />
        </div>
      </template>

      <template #cell(hinst)="{ rowData }">
        {{ getHints(rowData.id) }}
      </template>

      <template #headerPrepend>
        <tr class="table-crud__slot">
          <th class="p-1 min-w-[150px]">
            Pula
          </th>
          <th class="p-1 min-w-[150px]">
            -
          </th>
          <th class="p-1 min-w-[150px] justify-center">
            {{ getMoney("money_pool") }}
          </th>
          <th class="p-1 min-w-[150px]">
            {{ adminScoresAuctioned }}
          </th>
          <th class="p-1 min-w-[150px]">
            <VaInput
              tabindex="1"
              v-model="adminScoresAddon"
            />
          </th>
          <th class="p-1 min-w-[150px]">
            <VaButton block @click="endAuction">
              Przelicz
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
