import { ref, computed } from 'vue'
import { defineStore } from "pinia"
import { Status, sleep } from '@/base/basestore'
import { timerUrl } from '@/base/urls'

import jwtCall from "@/auth/calls"

export default (playId) => defineStore("timer_" + playId, () => {
  const baseServer = ref(null)
  const basePerf = ref(null)
  const timer = ref(null)
  const now = ref(0)
  let tickTimer = null

  const serverNow = () => {
    return baseServer.value + (performance.now() - basePerf.value)
  }

  const refresh = async () => {
    const samples = []
    for (let index = 0; index < 5; index++) {
      const t0 = performance.now()
      const { data, error, status } = await jwtCall({
        url: timerUrl(playId),
        method: "get",
      })

      const { server_time, timer } = data
      const t1 = performance.now()
      samples.push({ rtt: t1 - t0, server_time, t1, timer })
    }
    // we are fetching a sample from smallest RTT
    const best = samples.sort((a, b) => a.rtt - b.rtt)[0]
    baseServer.value = best.server_time + best.rtt / 2
    basePerf.value = best.t1
    timer.value = best.timer

  }

  const start = async (seconds) => {
    const ms = seconds * 1000
    await jwtCall({
      url: timerUrl(playId, 'start'),
      method: "post",
      data: {
        microseconds: ms
      }
    })
    await refresh()
  }

  const stop = async () => {
    await jwtCall({
      url: timerUrl(playId, 'stop'),
      method: "post",
    })
    await refresh()
  }

  const runOnMounted = async () => {
    await refresh()

    tickTimer = setInterval(() => {
      now.value = serverNow()
    }, 100)
  }

  const runOnBeforeUnmount = async () => {
    if(tickTimer) {
      clearInterval(tickTimer)
      tickTimer = null
    }
  }


  return {timer, refresh, now, start, stop, runOnMounted, runOnBeforeUnmount}

})
