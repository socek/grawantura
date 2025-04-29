import { ref, computed } from 'vue'
import { defineStore } from "pinia"
import { Status } from '@/base/basestore'
import { hostUrl } from '@/base/urls'

import jwtCall from "@/auth/calls"

export default (playId) => defineStore("host_" + playId, () => {
  const question = ref({})
  const questionStatus = ref(Status.BeforeLoad)

  async function fetchQuestion(force) {
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
    questionStatus,
    fetchQuestion,
  }
})

