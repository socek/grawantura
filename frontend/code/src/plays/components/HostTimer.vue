<script setup>
  import { ref, computed, onBeforeUnmount, onMounted, onUnmounted } from 'vue';
  import { useToast } from 'vuestic-ui'
  import colors from '@/base/colors'
  import useTimerStore from '@/timer/store'

  const props = defineProps(['playId'])

  const timerStore = useTimerStore(props.playId)()

  const isTimerStarted = computed(() => {
    return Boolean(timerStore.timer && timerStore.timer.status === 'running')
  })

  const canStopTimer = computed(() => {
    if (Boolean(timerStore.timer && timerStore.timer.status === 'running')) {
      const seconds = (timerStore.timer.end_time - timerStore.now) / 1000
      if(seconds > 0) {
        return false
      }
    }
    return true
  })

  const formattedTime = computed(() => {
    if (isTimerStarted.value) {
      const seconds = (timerStore.timer.end_time - timerStore.now) / 1000
      if(seconds <= 0) {
        return '(zakończony)'
      }
      const visibleSeconds = Math.floor(seconds + 1)
      const visibleMinutes = Math.floor((seconds + 1) / 60)
      return `${String(visibleMinutes % 60).padStart(2, '0')}m ${String(visibleSeconds % 60).padStart(2, '0')}s`
    }

    return '(zatrzymany)'

  });

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

  const cssBar = () => {
    const cssDict = {}
    if (isTimerStarted.value) {
      const currentSeconds = (timerStore.timer.end_time - timerStore.now) / 1000
      const maxSeconds = 60
      const percent = currentSeconds / maxSeconds * 100
      cssDict["background"] = `linear-gradient(90deg, #3b82f6 ${percent}%, transparent ${percent}%)`
      cssDict["color"] = 'red'
    }
    return cssDict
  }

  onMounted(async () => {
    await timerStore.refresh()
  })

</script>

<template>
  <VaCard class="counterBox">
    <VaCardTitle>Licznik</VaCardTitle>
    <VaCardContent>
      <div :style="cssBar()">{{ formattedTime }}</div>
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
