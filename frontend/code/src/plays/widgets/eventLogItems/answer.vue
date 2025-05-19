<script setup>
  import { ref } from 'vue'
  import deleteEvent from '@/plays/widgets/eventLogItems/deleteEvent.vue'

  const props = defineProps(['playId', 'event'])
  const success = ref(props.event['payload']['success'])
</script>

<template>
  <VaListItem class="list__item goup">
    <div class="row outline">
        <div class="item success" v-if="success">
          Dobra Odpowiedź <deleteEvent :eventId="props.event['id']" :playId="props.playId" />
        </div>
        <div class="item fail" v-if="!success">
          Zła Odpowiedź <deleteEvent :eventId="props.event['id']" :playId="props.playId" />
        </div>
    </div>
  </VaListItem>
</template>

<style scopes>
  .goup {
    margin-top: -100px;
    padding-top: -100px;
  }
  .row {
    width: 100%;
  }
  .success {
    font-weight: bold;
    color: rgb(255, 255, 255);
    background-color: #228200;
  }
  .fail {
    font-weight: bold;
    color: rgb(255, 255, 255);
    background-color: #E42222;
  }
</style>
