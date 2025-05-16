<script setup>
  import deleteEvent from '@/plays/widgets/eventLogItems/deleteEvent.vue'

  const props = defineProps(['playId', 'event'])
</script>

<template>
  <VaListItem class="list__item">
    hint <deleteEvent :playId="event['id']" />
  </VaListItem>
</template>
