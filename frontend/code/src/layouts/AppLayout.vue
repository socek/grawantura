<template>
  <VaLayout
    :top="{ fixed: true, order: 2 }"
    :left="{ fixed: true, absolute: breakpoints.mdDown, order: 1, overlay: breakpoints.mdDown }"
  >
    <template #top>
      <AppNavbar />
    </template>

    <template #content>
      <main class="p-4 pt-0">
        <article>
          <RouterView :key="Route.fullPath" />
        </article>
      </main>
    </template>
  </VaLayout>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useBreakpoint } from 'vuestic-ui'

import AppNavbar from '../components/navbar/AppNavbar.vue'

const breakpoints = useBreakpoint()

const Route = useRouter()

</script>

