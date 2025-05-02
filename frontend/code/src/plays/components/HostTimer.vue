<script setup>
  import { ref } from 'vue'

  const props = defineProps(['playId'])
  const value = ref()
</script>

<template>
  <VaCard>
    <VaCardTitle>Licznik</VaCardTitle>
    <VaCardContent>
      <VaTimeInput readonly v-model="value" class="w-28" />
    </VaCardContent>
    <VaCardActions align="stretch" vertical>
      <VaButton color="success">Start</VaButton>
      <VaButton color="danger">Stop</VaButton>
      <VaButton color="warning">Reset</VaButton>
    </VaCardActions>
  </VaCard>
</template>
