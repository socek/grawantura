import { ref, computed } from 'vue'
import { defineStore } from "pinia"
import { Status, sleep } from '@/base/basestore'
import { hostUrl } from '@/base/urls'

import jwtCall from "@/auth/calls"

export const useHostQuestionStore = (playId) => defineStore("question_" + playId, () => {
  const question = ref({})
  const isStarted = ref(false)
  const status = ref(Status.BeforeLoad)

  const moneyPool = ref({})
  const auctionedPool = ref({})
  const addonPool = ref({})
  const hints = ref({})
  const answeringTeamId = ref(null)
  const showHint = ref(false)
  const answerStatus = ref(false)
  const events = ref([])
  const gameId = ref(null)

  async function fetch(force) {
    force = force || false
    if (!force && status.value != Status.BeforeLoad) {
      while(status.value != Status.Completed) {
        await sleep(300)
      }
      return
    }
    status.value = Status.Loading
    moneyPool.value = {}
    auctionedPool.value = {}
    addonPool.value = {}
    hints.value = {}
    answeringTeamId.value = null
    showHint.value = false
    answerStatus.value = false
    events.value = []
    gameId.value = null
    try {
      const { data, error, reqstatus } = await jwtCall({
        url: hostUrl(playId, 'question'),
        method: "get",
      })

      if (error && reqstatus !== 406) throw error
      if (data) {
        question.value = data.question
        isStarted.value = data.is_started
        for (const [key, value] of Object.entries(data.money)) {
          moneyPool.value[key] = value
          auctionedPool.value[key] = 0
          addonPool.value[key] = 0
        }
        hints.value = data.hints
        answeringTeamId.value = data.answering_team_id
        showHint.value = data.show_hint
        answerStatus.value = data.answer_status
        events.value = data.events
        gameId.value = data.game_id
        status.value = Status.Completed
      } else {
        status.value = Status.Failed
      }
    } catch (error) {
      status.value = Status.Failed
    }
  }

  return {
    question,
    isStarted,
    status,
    fetch,
    moneyPool,
    auctionedPool,
    addonPool,
    hints,
    answeringTeamId,
    showHint,
    answerStatus,
    events,
    gameId,
  }
})

export const useHostViewStore = (playId) => defineStore("view_" + playId, () => {
  const payload = ref({})
  const status = ref(Status.BeforeLoad)

  async function clear() {
    status.value = Status.BeforeLoad
  }

  async function fetch(force) {
    force = force || false
    if (!force && status.value != Status.BeforeLoad) {
      while(status.value != Status.Completed) {
        await sleep(300)
      }
      return
    }
    status.value = Status.Loading
    try {
      const { data, error, reqstatus } = await jwtCall({
        url: hostUrl(playId, 'view'),
        method: "get",
      })
      if (error && reqstatus !== 406) throw error
      if (data) {
        payload.value = data
        status.value = Status.Completed
      } else {
        status.value = Status.Failed
      }
    } catch (error) {
      status.value = Status.Failed
    }
  }

  return {
    payload,
    status,
    fetch,
    clear,
  }
})

