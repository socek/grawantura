<script setup>
  import Router from "@/router"

  const props = defineProps(['gameId'])
  const onClick = () => {
    Router.push({ name: 'plays', params: { gameId: props.gameId } })
  }
</script>

<template>
  <div>
    <VaPopover message="Go To Plays">
      <VaButton
        preset="primary"
        color="success"
        size="small"
        aria-label="Go To Plays"
        @click="onClick"
      >
        <VaIcon class="material-icons">
          play_circle_filled
        </VaIcon>
      </VaButton>
    </VaPopover>
  </div>
</template>
