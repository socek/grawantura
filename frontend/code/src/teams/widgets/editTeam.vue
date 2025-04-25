<script setup>
  import { ref } from 'vue'
  import { validators } from '@/services/utils'
  import { useModal, useForm } from 'vuestic-ui'
  import { isEqual } from 'lodash';
  import useTeamStore from '@/teams/store'
  import commands from "@/teams/commands"

  const props = defineProps(['playId', 'itemId'])
  const teamStore = useTeamStore(props.playId)()
  const { confirm } = useModal()
  const form = useForm('edit-team-form')

  const isVisible = ref(false)

  const defaultTeamData = () => {
    return teamStore.items.filter(item => {
      return item.id == props.itemId
    })[0]
  }

  const teamData = ref({ ...defaultTeamData() })

  const onCancel = async () => {
    if (!isEqual(teamData.value, defaultTeamData())) {
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
      await commands.updateTeam({
        "playId": props.playId,
        "teamId": props.itemId,
        "name": teamData.value.name,
      })
      isVisible.value = false
    }
  }

  const showDialog = () => {
    teamData.value = { ...defaultTeamData() }
    isVisible.value = true
  }
</script>

<template>
  <div>
    <VaPopover message="Edit team">
      <VaButton
        preset="primary"
        size="small"
        aria-label="Edit team"
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
      <h1 class="va-h5">Edit Team</h1>
      <VaForm v-slot="{ isValid }" ref="edit-team-form" class="flex-col justify-start items-start gap-4 inline-flex w-full">
        <div class="self-stretch flex-col justify-start items-start gap-4 flex">
          <div class="flex gap-4 flex-col sm:flex-row w-full">
            <VaInput
              v-model="teamData.name"
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
