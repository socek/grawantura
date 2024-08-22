<script setup>
import { onMounted, ref } from 'vue'
import { supabase } from './supabase'
import { useRoute } from 'vue-router'

const session = ref()

onMounted(() => {
  // supabase.auth.getSession().then(({ data }) => {
  //   session.value = data.session
  // })

  // supabase.auth.onAuthStateChange((_, _session) => {
  //   session.value = _session
  // })
  // const route = useRoute()

  // console.log(route.params)
})
</script>

<template>
  <div class="container" style="padding: 50px 0 100px 0">
    <nav>
      <RouterLink to="/">Home</RouterLink>
    </nav>
    <main>
      <RouterView />
    </main>

  </div>
</template>
