<script setup>
  import { computed, onMounted, onBeforeUnmount } from 'vue'
  import useTimerStore from '@/timer/store'

  // Large timer for the game screen (/play). The host dashboard keeps using
  // the small @/timer/components/timer.vue.
  const props = defineProps(['playId'])
  const timerStore = useTimerStore(props.playId)()

  // Same full duration the host starts ("Start 60 s").
  const MAX_SECONDS = 60

  const isRunning = computed(() => {
    return Boolean(timerStore.timer && timerStore.timer.status === 'running')
  })

  const secondsLeft = computed(() => {
    if (!isRunning.value) {
      return MAX_SECONDS
    }
    const seconds = (timerStore.timer.end_time - timerStore.now) / 1000
    return Math.max(0, seconds)
  })

  const isFinished = computed(() => isRunning.value && secondsLeft.value <= 0)
  const isEnding = computed(() => isRunning.value && !isFinished.value && secondsLeft.value <= 10)

  const formattedTime = computed(() => {
    // Round up, so "00:00" shows only when time is really up.
    const total = Math.ceil(secondsLeft.value)
    const minutes = Math.floor(total / 60)
    const seconds = total % 60
    return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
  })

  const progressStyle = computed(() => {
    const percent = Math.min(100, secondsLeft.value / MAX_SECONDS * 100)
    return { width: `${percent}%` }
  })

  onMounted(timerStore.runOnMounted)
  onBeforeUnmount(timerStore.runOnBeforeUnmount)
</script>

<template>
  <div
    class="play-timer"
    :class="{ stopped: !isRunning, ending: isEnding, finished: isFinished }"
  >
    <div class="progress" v-if="isRunning" :style="progressStyle"></div>
    <span class="content">
      <span class="material-icons icon" v-if="!isRunning">pause</span>
      <span class="time">{{ formattedTime }}</span>
    </span>
  </div>
</template>

<style scoped>
  .play-timer {
    position: relative;
    overflow: hidden;
    height: 100%;
    min-width: 18vw;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1vh 2vw;
    box-sizing: border-box;
    border-radius: 1.5rem;
    background: rgba(255, 255, 255, 0.12);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    transition: opacity 0.3s, background 0.3s;
  }

  .progress {
    position: absolute;
    inset: 0 auto 0 0;
    background: linear-gradient(90deg, #22d3ee, #3b82f6);
    transition: width 0.1s linear, background 0.3s;
  }
  .ending .progress {
    background: linear-gradient(90deg, #f97316, #ef4444);
  }

  .content {
    position: relative;
    display: flex;
    align-items: center;
    gap: 1vw;
  }

  .time {
    font-weight: 800;
    font-size: clamp(1.5rem, 3.5vw, 3.5rem);
    font-variant-numeric: tabular-nums;
    line-height: 1.1;
  }

  .icon {
    font-size: clamp(1.5rem, 3.5vw, 3.5rem);
  }

  .stopped {
    opacity: 0.5;
  }

  .finished {
    background: linear-gradient(135deg, #ef4444, #b91c1c);
    animation: pulse 1s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
  }
</style>
