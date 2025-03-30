<script setup>
  import axios from 'axios'
  import { onMounted, ref, toRaw } from 'vue'
  import { validators } from '@/services/utils'
  import { useModal, useForm } from 'vuestic-ui'
  import { isEqual } from 'lodash';
  import commands from '@/pages/admin/games/commands'

  const { confirm } = useModal()
  const form = useForm('create-game-form')

  const defaultNewGame = {
    name: '',
  }

  const newGame = ref({ ...defaultNewGame })
  const doShowAddGame = ref(false)

  const onCancel = async () => {
    if (!isEqual(newGame.value, defaultNewGame)) {
      const agreed = await confirm({
        maxWidth: '380px',
        message: 'Form has unsaved changes. Are you sure you want to close it?',
        size: 'small',
      })
      if (agreed) {
        doShowAddGame.value = false
      }
    } else {
      doShowAddGame.value = false
    }
  }

  const onSave = async () => {
    if (form.validate()) {
      await commands.createGame({...newGame.value})
      doShowAddGame.value = false
    }
  }

  const showDialog = () => {
    newGame.value = { ...defaultNewGame }
    doShowAddGame.value = true
  }
</script>

<template>
  <div>
    <VaButton @click="showDialog">Add Game</VaButton>

    <VaModal
      v-model="doShowAddGame"
      size="small"
      mobile-fullscreen
      close-button
      hide-default-actions
    >
      <h1 class="va-h5">Create Game</h1>
      <VaForm v-slot="{ isValid }" ref="create-game-form" class="flex-col justify-start items-start gap-4 inline-flex w-full">
        <div class="self-stretch flex-col justify-start items-start gap-4 flex">
          <div class="flex gap-4 flex-col sm:flex-row w-full">
            <VaInput
              v-model="newGame.name"
              label="Name"
              class="w-full"
              :rules="[validators.required]"
              name="name"
            />
          </div>

          <div class="flex gap-2 flex-col-reverse items-stretch justify-end w-full sm:flex-row sm:items-center">
            <VaButton preset="secondary" color="secondary" @click="onCancel">Cancel</VaButton>
            <VaButton :disabled="!isValid" @click="onSave">Save</VaButton>
          </div>
        </div>
      </VaForm>
    </VaModal>
  </div>
</template>
