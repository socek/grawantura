<script setup>
  import { onMounted, ref, computed } from 'vue'
  import { supabase } from './models/supabase'

  import { useStore } from 'vuex'
  const store = useStore()

  const isAuthenticated = computed(() => {
    return store.getters["auth/isAuthenticated"]
  })

  onMounted(async () => {
    await store.dispatch("auth/init")
  })
</script>

<template>
  <div class="container" style="padding: 50px 0 100px 0">
    <nav>
      <div><RouterLink to="/">Home</RouterLink></div>
      <div v-if="!isAuthenticated"><RouterLink to="/login">Login</RouterLink></div>
      <div v-if="isAuthenticated"><RouterLink to="/account">Account</RouterLink></div>
      <div><RouterLink to="/editor">Panel Edytora</RouterLink></div>
    </nav>
    <main>
      <RouterView />
    </main>

  </div>
</template>

<style>
nav div {
  float: left;
  padding-left: 5px;
  padding-right: 5px;
}
</style>
