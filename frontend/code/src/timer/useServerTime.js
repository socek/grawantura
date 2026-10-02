import { ref, onMounted, onUnmounted } from 'vue'

import { timerUrl } from '@/base/urls'
import jwtCall from "@/auth/calls"

export function useServerTime(playId, syncEveryMs = 30000) {
  // punkt odniesienia: czas serwera i zegar monotoniczny przeglądarki
  let baseServer = null
  let basePerf = null
  let baseTimer = null
  const now = ref(0)
  const timer = ref(null)
  let syncTimer, tickTimer

  async function sync() {
    const samples = []
    for (let i = 0; i < 5; i++) {
      const t0 = performance.now()
      const { data, error, status } = await jwtCall({
        url: timerUrl(playId),
        method: "get",
      })

      const { server_time, timer } = data
      const t1 = performance.now()
      samples.push({ rtt: t1 - t0, server_time, t1, timer })
    }
    // bierzemy próbkę z najkrótszym RTT (najdokładniejszą)
    const best = samples.sort((a, b) => a.rtt - b.rtt)[0]
    baseServer = best.server_time + best.rtt / 2
    basePerf = best.t1
    baseTimer = best.timer
  }

  // aktualny czas serwera w ms
  function serverNow() {
    return baseServer + (performance.now() - basePerf)
  }

  const refresh = async () => {
    await sync()
    now.value = serverNow()
    timer.value = baseTimer
    tickTimer = setInterval(() => (now.value = serverNow()), 100)
    syncTimer = setInterval(sync, syncEveryMs)
  }

  onMounted(refresh)

  onUnmounted(() => {
    clearInterval(tickTimer)
    clearInterval(syncTimer)
  })

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

  return { now, serverNow, timer, start, stop }
}
