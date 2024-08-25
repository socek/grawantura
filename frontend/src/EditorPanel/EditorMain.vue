<script setup>
  import { onMounted, ref, computed } from 'vue'
  import { useStore } from 'vuex'
  import { Status } from '../models/consts'
  import { supabase } from '../models/supabase'

  const showCreate = ref(false)
  const formError = ref('')
  const createForm = ref({
    name: ''
  })

  const store = useStore()

  const isLoaded = computed(() => {
    return store.getters["games/getStatus"] == Status.Completed
  })
  const games = computed(() => {
    return store.getters["games/getItems"]
  })

  onMounted(async () => {
    store.dispatch("games/fetch")
  })

  const onSubmit = async (event) => {
    event.preventDefault()

    try {
      const { data, error } = await supabase
        .from('games')
        .insert([createForm.value])

      if (error) throw error

      store.dispatch("games/fetch", true)
      createForm.value.name = ''
      showCreate.value = false
      formError.value = ''
    } catch (error) {
      formError.value = error.message
      console.log(error)
    }
  }
</script>

<template>
  <div>
    <h1>Panel Edytora</h1>
    <p @click="showCreate = !showCreate">Stwórz Grę</p>
    <div id="createDialog" v-if="showCreate">
      <p v-if="formError">{{ formError }}</p>
      <form @submit="onSubmit">
        <div>Nazwa: <input v-model="createForm.name" /></div>
        <div><button>Zapisz</button></div>
      </form>
    </div>
    <ul v-if="isLoaded">
      <li v-for="game in games" :key="game.id">{{ game.name }}</li>
    </ul>
    <div v-else>
      Loading...
    </div>
  </div>
</template>

<style>
  #createDialog {
    border: 1px black solid;
    padding: 10px;
  }
</style>
