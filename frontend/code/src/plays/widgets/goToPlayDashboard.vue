<script setup>
  import Router from "@/router"

  const props = defineProps(['itemId'])
  const onClick = () => {
    Router.push({ name: 'playDashboard', params: { playId: props.itemId } })
  }
</script>

<template>
  <div>
    <VaPopover message="Go To Play Dashboard">
      <VaButton
        preset="primary"
        color="success"
        size="small"
        aria-label="Go To Play Dashboard"
        @click="onClick"
      >
        <VaIcon class="material-icons">open_with</VaIcon>
      </VaButton>
    </VaPopover>
  </div>
</template>
