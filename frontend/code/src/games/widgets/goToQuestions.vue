<script setup>
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
