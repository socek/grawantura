<script setup>
  import { onMounted, onUnmounted, ref } from 'vue'
  import axios from 'axios'

  let lastTime = null;
  let cycleReference = null;

  const fetchData = async () => {
    const res = await axios.get(
      '/api/events',
      {
          params: {"time": lastTime}
      }
    )
    res.data.elements.forEach(async (element) => {
      console.log(element)
    })
    lastTime = res.data.time
  }

  onMounted(async () => {
    const res = await axios('/api/events')
    console.log(res.data)
    lastTime = res.data.time
    cycleReference = setInterval(fetchData, 1000)
  })

  onUnmounted(async () => {
    clearInterval(cycleReference)
  })
</script>

<template>
</template>
