import { defineStore } from "pinia"
import { ref, computed } from 'vue'

import { JWT_TOKEN_KEY } from "./consts"

export default defineStore("auth", () => {
  const jwtToken = ref(null)
  const getToken = computed(() => jwtToken.value)
  const isAuthorized = computed(() => jwtToken.value != null)

  function setToken(jwtTokenValue) {
    jwtToken.value = jwtTokenValue
    localStorage.setItem(JWT_TOKEN_KEY, jwtTokenValue)
  }

  function clearToken() {
    jwtToken.value = null
    localStorage.removeItem(JWT_TOKEN_KEY)
  }

  if (localStorage.getItem(JWT_TOKEN_KEY)) {
    jwtToken.value = localStorage.getItem(JWT_TOKEN_KEY);
  }

  return {
    jwtToken,
    getToken,
    isAuthorized,
    setToken,
    clearToken,
  }
})
