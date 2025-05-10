<script setup>
  import { validators } from '@/services/utils'
  import { computed, onMounted, ref } from 'vue'
  import { Status } from '@/base/basestore'
  import { useHostQuestionStore } from "@/plays/hoststore"
  import useTeamStore from '@/teams/store'
  import { useForm } from 'vuestic-ui'
  import commands from "@/plays/commands"

  const props = defineProps(['playId'])
  const questionStore = useHostQuestionStore(props.playId)()
  const teamStore = useTeamStore(props.playId)()

  const dialogVisible = ref(false)
  const formData = ref({})
  const form = useForm('start-game-form')

  onMounted(async () => {
    await questionStore.fetch()
    await teamStore.fetch()
  })

  const isStarted = computed(() => {
    return questionStore.isStarted
  })

  const teams = computed(() => teamStore.items)

  const isLoading = computed(() => {
    return [Status.BeforeLoad, Status.Loading].indexOf(questionStore.questionStatus) != -1
  })

  const showDialog = async () => {
    formData.value = {}
    teams.value.forEach((row, index) => {
      formData.value[row.id] = 5000
    })
    console.log(formData.value)
    dialogVisible.value = true
  }

  const onCancel = async () => {
    dialogVisible.value = false
  }

  const onSave = async () => {
    if (form.validate()) {
      for (const [key, value] of Object.entries(formData.value)) {
        formData.value[key] = parseInt(value)
      }
      await commands.startGame(props.playId, formData.value)
      console.log(formData.value)
      dialogVisible.value = false
    }
  }
</script>

<template>
  <div>
    <VaButton
      :loading="isLoading"
      :disabled="isStarted"
      color="warning"
      @click="showDialog">Start game</VaButton>

      <VaModal
        v-model="dialogVisible"
        size="small"
        mobile-fullscreen
        close-button
        hide-default-actions
      >
        <h1 class="va-h5">Start Play</h1>
        <VaForm v-slot="{ isValid }" ref="start-game-form" class="flex-col justify-start items-start gap-4 inline-flex w-full">
          <div class="self-stretch flex-col justify-start items-start gap-4 flex">
            <div class="flex gap-4 flex-col sm:flex-row w-full" v-for="team in teams" :key="team.id">
              <VaInput
                v-model="formData[team.id]"
                :label="team.name"
                class="w-full"
                :rules="[validators.required]"
                :name="team.id"
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
