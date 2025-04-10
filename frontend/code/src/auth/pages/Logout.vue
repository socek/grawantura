<template>
  <div>
    <h1 class="font-semibold text-4xl mb-4">Loged out</h1>
  </div>
</template>

<script setup>
  import { onMounted } from 'vue'
  import useAuthStore from '@/auth/store'
  import { useToast } from 'vuestic-ui'
  import Router from "@/router"

  const authStore = useAuthStore()
  const { init } = useToast()

  onMounted(() => {
    authStore.clearToken()
    init({"message": "Logged out"})
    Router.push({ name: 'login'})
  })
</script>
