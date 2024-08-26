<script setup>
  import { ref } from 'vue'
  import { supabase } from '../../models/supabase'
  import { useStore } from 'vuex'

  const store = useStore()

  const showCreate = ref(false)
  const formError = ref('')
  const createForm = ref({
    name: ''
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
    <p @click="showCreate = !showCreate">Stwórz Grę</p>
    <div id="createDialog" v-if="showCreate">
      <p v-if="formError">{{ formError }}</p>
      <form @submit="onSubmit">
        <div>Nazwa: <input v-model="createForm.name" /></div>
        <div><button>Zapisz</button></div>
      </form>
    </div>
  </div>
</template>

<style>
  #createDialog {
    border: 1px black solid;
    padding: 10px;
  }
</style>
