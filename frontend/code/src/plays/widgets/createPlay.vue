<script setup>
  import { ref } from 'vue'
  import { validators } from '@/services/utils'
  import { useModal, useForm } from 'vuestic-ui'
  import { isEqual } from 'lodash';
  import commands from "@/plays/commands"

  const props = defineProps(['gameId'])
  const { confirm } = useModal()
  const form = useForm('create-play-form')

  const defaultNewPlay = {
    gameId: props.gameId,
    name: '',
  }

  const newPlay = ref({ ...defaultNewPlay })
  const doShowAddPlay = ref(false)

  const onCancel = async () => {
    if (!isEqual(newPlay.value, defaultNewPlay)) {
      const agreed = await confirm({
        maxWidth: '380px',
        message: 'Form has unsaved changes. Are you sure you want to close it?',
        size: 'small',
      })
      if (agreed) {
        doShowAddPlay.value = false
      }
    } else {
      doShowAddPlay.value = false
    }
  }

  const onSave = async () => {
    if (form.validate()) {
      await commands.createPlay({...newPlay.value})
      doShowAddPlay.value = false
    }
  }

  const showDialog = () => {
    newPlay.value = { ...defaultNewPlay }
    doShowAddPlay.value = true
  }
</script>

<template>
  <div>
    <VaButton @click="showDialog">Add Play</VaButton>

    <VaModal
      v-model="doShowAddPlay"
      size="small"
      mobile-fullscreen
      close-button
      hide-default-actions
    >
      <h1 class="va-h5">Create Play</h1>
      <VaForm v-slot="{ isValid }" ref="create-play-form" class="flex-col justify-start items-start gap-4 inline-flex w-full">
        <div class="self-stretch flex-col justify-start items-start gap-4 flex">
          <div class="flex gap-4 flex-col sm:flex-row w-full">
            <VaInput
              v-model="newPlay.name"
              label="Play"
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
