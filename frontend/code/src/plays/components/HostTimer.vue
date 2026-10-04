<script setup>
  import { computed } from 'vue';
  import useTimerStore from '@/timer/store'
  import Timer from "@/timer/components/timer.vue"

  const props = defineProps(['playId'])

  const timerStore = useTimerStore(props.playId)()

  const canStopTimer = computed(() => {
    if (Boolean(timerStore.timer && timerStore.timer.status === 'running')) {
      const seconds = (timerStore.timer.end_time - timerStore.now) / 1000
      if(seconds > 0) {
        return false
      }
    }
    return true
  })

  const startButtonColor = computed(() => {
    if(canStopTimer.value) {
      return 'success'
    } else {
      return 'warning'
    }
  })

  const startButtonAction = async () => {
    await timerStore.start(60)
  }

  const stopButtonAction = async () => {
    await timerStore.stop()
  }

</script>

<template>
  <VaCard class="counterBox">
    <VaCardTitle>Zegar </VaCardTitle>
    <VaCardContent>
      <Timer :playId="props.playId" />
    </VaCardContent>

    <VaCardActions align="stretch" vertical>
      <VaButton @click="startButtonAction()" :color="startButtonColor">Start 60 s</VaButton>
      <VaButton :disabled="canStopTimer" @click="stopButtonAction()">Stop</VaButton>
    </VaCardActions>
  </VaCard>
</template>

<style scoped>
  .counterBox {
    width: 150px;
  }
</style>
