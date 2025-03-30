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
    lastTime = res.data.time
    console.log(res.data)
    cycleReference = setInterval(fetchData, 1000)
  })

  onUnmounted(async () => {
    clearInterval(cycleReference)
  })
</script>

<template>
</template>
