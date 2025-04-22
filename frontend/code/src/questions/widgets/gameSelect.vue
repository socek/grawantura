<template>
  <div class="max-w-xs">
    <VaSelect
      v-model="value"
      label="Game"
      :options="options"
      searchable
      highlight-matched-text
      track-by="value"
      @update:modelValue="onUpdate"
    />
  </div>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue'
  import useGamesStore from '@/games/store'
  import { useRouter } from 'vue-router'

  const Router = useRouter()

  const gamesStore = useGamesStore()
  const props = defineProps(['gameId', 'routeName'])

  const value = ref()
  const options = computed(() => {
    const result = []
    let currentRow = null;
    gamesStore.getItems.forEach((value, index) => {
      const row = {
        "text": value.name,
        "value": value.id,
      }
      result.push(row)
      if(row.value == props.gameId) {
        currentRow = row
      }
    })
    value.value = currentRow
    return result
  })
  const onUpdate = (event) => {
    Router.push({ name: props.routeName, params: { gameId: event.value } })
  }
  onMounted(async () => {
    await gamesStore.fetch()
  })
</script>
