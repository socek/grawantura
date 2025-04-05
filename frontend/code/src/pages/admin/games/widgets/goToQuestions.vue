<script setup>
  import { onMounted, ref, toRaw } from 'vue'
  import { validators } from '@/services/utils'
  import { useModal, useForm } from 'vuestic-ui'
  import { isEqual } from 'lodash';
  import useGamesStore from '@/pages/admin/games/store'
  import commands from '@/pages/admin/games/commands'
  import Router from "@/router"

  const props = defineProps(['gameId'])
  const onClick = () => {
    Router.push({ name: 'questions', params: { gameId: props.gameId } })
  }
</script>

<template>
  <div >
    <VaButton
      preset="primary"
      size="small"
      icon="mso-start"
      aria-label="Go To Questions"
      @click="onClick"
    />
  </div>
</template>
