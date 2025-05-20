<script setup>
  import { ref, computed, onBeforeUnmount } from 'vue';
  import { useToast } from 'vuestic-ui'
  import colors from '@/base/colors'

  const props = defineProps(['playId'])
  const { init: notify } = useToast()

  const defaultTime = 60000

  let targetTime = new Date().getTime() + defaultTime;
  const leftTotalSeconds = ref(defaultTime)
  const timeRemaining = ref(defaultTime);
  const counterRun = ref(false)

  const formattedTime = computed(() => {
    const seconds = Math.floor(timeRemaining.value / 1000);
    const minutes = Math.floor(seconds / 60);
    return `${String(minutes % 60).padStart(2, '0')}m ${String(seconds % 60).padStart(2, '0')}s`
  });

  const updateTimer = () => {
    timeRemaining.value = targetTime - new Date().getTime()
    if(timeRemaining.value <= 0) {
      clearInterval(intervalId)
      timeRemaining.value = 0
      leftTotalSeconds.value = 0
      counterRun.value = false

      notify({
        message: "Time finished!",
        color: colors.fail,
      })
    }
  }

  let intervalId
  const startCountdown = () => {
    targetTime = new Date().getTime() + leftTotalSeconds.value
    intervalId = setInterval(updateTimer, 500);
    counterRun.value = true
  }
  const stopCountdown = () => {
    clearInterval(intervalId);
    leftTotalSeconds.value = timeRemaining.value
    counterRun.value = false
  }
  const resetCountdown = () => {
    leftTotalSeconds.value = defaultTime
    timeRemaining.value = defaultTime
    clearInterval(intervalId)
    counterRun.value = false
  }

  onBeforeUnmount(() => {
    stopCountdown()
  })

</script>

<template>
  <VaCard class="counterBox">
    <VaCardTitle>Licznik</VaCardTitle>
    <VaCardContent>
      {{ formattedTime }}
    </VaCardContent>
    <VaCardActions align="stretch" vertical>
      <VaButton :disabled="counterRun || leftTotalSeconds == 0" color="success" @click="startCountdown">Start</VaButton>
      <VaButton :disabled="! counterRun" color="danger" @click="stopCountdown">Stop</VaButton>
      <VaButton color="warning" @click="resetCountdown">Reset</VaButton>
    </VaCardActions>
  </VaCard>
</template>

<style scoped>
  .counterBox {
    width: 150px;
  }
</style>
