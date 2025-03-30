import { defineStore } from "pinia"
import { ref, computed } from 'vue'

export default defineStore("auth", () => {
  const jwtToken = ref(null)
  const getToken = computed(() => jwtToken.value)
  const isAuthorized = computed(() => jwtToken.value != null)

  function setToken(jwtTokenValue) {
    jwtToken.value = jwtTokenValue
    localStorage.setItem('jwtToken', jwtTokenValue)
  }

  if (localStorage.getItem("jwtToken")) {
      jwtToken.value = localStorage.getItem("jwtToken");
    }

  return {
    jwtToken,
    getToken,
    isAuthorized,
    setToken,
  }
})
