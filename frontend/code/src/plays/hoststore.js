import { ref, computed } from 'vue'
import { defineStore } from "pinia"
import { Status } from '@/base/basestore'
import { hostUrl } from '@/base/urls'

import jwtCall from "@/auth/calls"

export const useHostQuestionStore = (playId) => defineStore("question_" + playId, () => {
  const question = ref({})
  const isStarted = ref(false)
  const questionStatus = ref(Status.BeforeLoad)

  const moneyPool = ref({})
  const auctionedPool = ref({})
  const addonPool = ref({})
  const hints = ref({})
  const answeringTeamId = ref(null)
  const showHint = ref(false)

  async function fetch(force) {
    force = force || false
    if (!force && questionStatus.value == Status.Completed) {
      return
    }
    questionStatus.value = Status.Loading
    moneyPool.value = {}
    auctionedPool.value = {}
    addonPool.value = {}
    hints.value = {}
    answeringTeamId.value = null
    showHint.value = false
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
        questionStatus.value = Status.Completed
      } else {
        questionStatus.value = Status.Failed
      }
    } catch (error) {
      questionStatus.value = Status.Failed
    }
  }

  return {
    question,
    isStarted,
    questionStatus,
    fetch,
    moneyPool,
    auctionedPool,
    addonPool,
    hints,
    answeringTeamId,
    showHint,
  }
})

export const useHostViewStore = (playId) => defineStore("view_" + playId, () => {
  const payload = ref({})
  const fetchStatus = ref(Status.BeforeLoad)

  async function clear() {
    fetchStatus.value = Status.BeforeLoad
  }

  async function fetch(force) {
    force = force || false
    if (!force && fetchStatus.value == Status.Completed) {
      return
    }
    fetchStatus.value = Status.Loading
    try {
      const { data, error, reqstatus } = await jwtCall({
        url: hostUrl(playId, 'view'),
        method: "get",
      })
      if (error && reqstatus !== 406) throw error
      if (data) {
        payload.value = data
        fetchStatus.value = Status.Completed
      } else {
        fetchStatus.value = Status.Failed
      }
    } catch (error) {
      fetchStatus.value = Status.Failed
    }
  }

  return {
    payload,
    fetchStatus,
    fetch,
    clear,
  }
})

