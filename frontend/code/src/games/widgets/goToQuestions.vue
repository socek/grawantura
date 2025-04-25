<script setup>
  import Router from "@/router"

  const props = defineProps(['gameId'])
  const onClick = () => {
    Router.push({ name: 'questions', params: { gameId: props.gameId } })
  }
</script>

<template>
  <div>
    <VaPopover message="Go To Questions">
      <VaButton
        preset="primary"
        color="success"
        size="small"
        aria-label="Go To Questions"
        @click="onClick"
      >
        <VaIcon class="material-icons">
          help
        </VaIcon>
      </VaButton>
    </VaPopover>
  </div>
</template>
