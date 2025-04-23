<script setup>
  import Router from "@/router"

  const props = defineProps(['itemId'])
  const onClick = () => {
    Router.push({ name: 'playDashboard', params: { playId: props.itemId } })
  }
</script>

<template>
  <div >
    <VaButton
      preset="primary"
      size="small"
      icon="star"
      aria-label="Go To Play Dashboard"
      @click="onClick"
    />
  </div>
</template>
