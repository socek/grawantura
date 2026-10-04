<script setup>
  import { computed, onMounted, onUnmounted, onBeforeUnmount } from 'vue';
  import useTimerStore from '@/timer/store'

  const props = defineProps(['playId'])

  const timerStore = useTimerStore(props.playId)()

  const isTimerStarted = computed(() => {
    return Boolean(timerStore.timer && timerStore.timer.status === 'running')
  })

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

  onMounted(timerStore.runOnMounted)

  onBeforeUnmount(timerStore.runOnBeforeUnmount)
</script>

<template>
  <div :style="cssBar()">{{ formattedTime }}</div>
</template>
