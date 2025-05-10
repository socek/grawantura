import { ref, computed } from 'vue'
import { defineStore } from "pinia"
import { Status } from '@/base/basestore'
import { hostUrl } from '@/base/urls'

import jwtCall from "@/auth/calls"

export const useHostQuestionStore = (playId) => defineStore("question_" + playId, () => {
  const question = ref({})
  const isStarted = ref(false)
  const moneyPool = ref({})
  const questionStatus = ref(Status.BeforeLoad)

  async function fetch(force) {
    force = force || false
    if (!force && questionStatus.value == Status.Completed) {
      return
    }
    questionStatus.value = Status.Loading
    try {
      const { data, error, reqstatus } = await jwtCall({
        url: hostUrl(playId, 'question'),
        method: "get",
      })

      if (error && reqstatus !== 406) throw error
      if (data) {
        question.value = data.question
        moneyPool.value = data.money
        isStarted.value = data.is_started
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

