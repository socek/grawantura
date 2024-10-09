<script setup>
  import { onMounted, ref, toRaw } from 'vue'
  import { validators } from '@/services/utils'
  import { useModal, useForm, useToast } from 'vuestic-ui'
  import { isEqual } from 'lodash';
  import useGamesStore from '@/stores/games'
  import { supabase } from '@/stores/supabase'

  const props = defineProps(['item_id'])
  const gamesStore = useGamesStore()
  const { init: notify } = useToast()

  const { confirm } = useModal()
  const form = useForm('edit-game-form')
  const showForm = ref(false)

  const defaultGameData = () => {
    return gamesStore.items.filter(item => {
      return item.id == props.item_id
    })[0]
  }

  const gameData = ref({ ...defaultGameData() })
  const isVisible = ref(false)

  const onCancel = async () => {
    if (!isEqual(gameData.value, defaultGameData())) {
      const agreed = await confirm({
        maxWidth: '380px',
        message: 'Form has unsaved changes. Are you sure you want to close it?',
        size: 'small',
      })
      if (agreed) {
        isVisible.value = false
      }
    } else {
      isVisible.value = false
    }
  }

  const onSave = async () => {
    if (form.validate()) {
      const { error } = await supabase
        .from('games')
        .update({
          name: gameData.value.name
        })
        .eq("id", props.item_id)
      console.log(error)

      if (error) {
        notify({
          message: `Row save failed`,
          color: '#FF0000',
        })
      } else {
        notify({
          message: `Row saved!`,
          color: 'success',
        })
        console.log("Fetching emit")
        await gamesStore.fetch(true)
      }

      isVisible.value = false

    }
  }

  const showDialog = () => {
    gameData.value = { ...defaultGameData() }
    isVisible.value = true
  }
</script>

<template>
  <div class="flex gap-2 justify-end">
    <VaButton
      preset="primary"
      size="small"
      icon="mso-edit"
      aria-label="Edit user"
      @click="showDialog()"
    />

    <VaModal
      v-model="isVisible"
      size="small"
      mobile-fullscreen
      close-button
      hide-default-actions
    >
      <h1 class="va-h5">Edit Game</h1>
      <VaForm v-slot="{ isValid }" ref="edit-game-form" class="flex-col justify-start items-start gap-4 inline-flex w-full">
        <div class="self-stretch flex-col justify-start items-start gap-4 flex">
          <div class="flex gap-4 flex-col sm:flex-row w-full">
            <VaInput
              v-model="gameData.name"
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
