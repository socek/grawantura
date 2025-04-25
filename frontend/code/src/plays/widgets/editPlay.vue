<script setup>
  import { ref } from 'vue'
  import { validators } from '@/services/utils'
  import { useModal, useForm } from 'vuestic-ui'
  import { isEqual } from 'lodash';
  import usePlayStore from '@/plays/store'
  import commands from "@/plays/commands"

  const props = defineProps(['gameId', 'itemId'])
  const playStore = usePlayStore(props.gameId)()
  const { confirm } = useModal()
  const form = useForm('edit-play-form')

  const isVisible = ref(false)

  const defaultPlayData = () => {
    return playStore.items.filter(item => {
      return item.id == props.itemId
    })[0]
  }

  const playData = ref({ ...defaultPlayData() })

  const onCancel = async () => {
    if (!isEqual(playData.value, defaultPlayData())) {
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
      await commands.updatePlay({
        "gameId": props.gameId,
        "playId": props.itemId,
        "name": playData.value.name,
      })
      isVisible.value = false
    }
  }

  const showDialog = () => {
    playData.value = { ...defaultPlayData() }
    isVisible.value = true
  }
</script>

<template>
  <div>
    <VaPopover message="Edit play">
      <VaButton
        preset="primary"
        size="small"
        aria-label="Edit play"
        @click="showDialog()"
      >
        <VaIcon name="edit" />
      </VaButton>
    </VaPopover>

    <VaModal
      v-model="isVisible"
      size="small"
      mobile-fullscreen
      close-button
      hide-default-actions
    >
      <h1 class="va-h5">Edit Play</h1>
      <VaForm v-slot="{ isValid }" ref="edit-play-form" class="flex-col justify-start items-start gap-4 inline-flex w-full">
        <div class="self-stretch flex-col justify-start items-start gap-4 flex">
          <div class="flex gap-4 flex-col sm:flex-row w-full">
            <VaInput
              v-model="playData.name"
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
