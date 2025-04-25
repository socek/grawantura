<script setup>
  import { ref } from 'vue'
  import { validators } from '@/services/utils'
  import { useModal, useForm } from 'vuestic-ui'
  import { isEqual } from 'lodash';
  import commands from "@/teams/commands"

  const props = defineProps(['playId'])
  const { confirm } = useModal()
  const form = useForm('create-team-form')

  const defaultNewTeam = {
    playId: props.playId,
    name: '',
  }

  const newTeam = ref({ ...defaultNewTeam })
  const doShowAddTeam = ref(false)

  const onCancel = async () => {
    if (!isEqual(newTeam.value, defaultNewTeam)) {
      const agreed = await confirm({
        maxWidth: '380px',
        message: 'Form has unsaved changes. Are you sure you want to close it?',
        size: 'small',
      })
      if (agreed) {
        doShowAddTeam.value = false
      }
    } else {
      doShowAddTeam.value = false
    }
  }

  const onSave = async () => {
    if (form.validate()) {
      await commands.createTeam({...newTeam.value})
      doShowAddTeam.value = false
    }
  }

  const showDialog = () => {
    newTeam.value = { ...defaultNewTeam }
    doShowAddTeam.value = true
  }
</script>

<template>
  <div>
    <VaButton @click="showDialog">Add Team</VaButton>

    <VaModal
      v-model="doShowAddTeam"
      size="small"
      mobile-fullscreen
      close-button
      hide-default-actions
    >
      <h1 class="va-h5">Create Team</h1>
      <VaForm v-slot="{ isValid }" ref="create-team-form" class="flex-col justify-start items-start gap-4 inline-flex w-full">
        <div class="self-stretch flex-col justify-start items-start gap-4 flex">
          <div class="flex gap-4 flex-col sm:flex-row w-full">
            <VaInput
              v-model="newTeam.name"
              label="Team"
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
