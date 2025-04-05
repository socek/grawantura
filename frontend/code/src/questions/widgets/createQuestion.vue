<script setup>
  import { ref } from 'vue'
  import { validators } from '@/services/utils'
  import { useModal, useForm } from 'vuestic-ui'
  import { isEqual } from 'lodash';
  import commands from "@/questions/commands"

  const props = defineProps(['gameId'])
  const { confirm } = useModal()
  const form = useForm('create-question-form')

  const defaultNewQuestion = {
    gameId: props.gameId,
    question: '',
    answer: '',
    hints: '',
  }

  const newQuestion = ref({ ...defaultNewQuestion })
  const doShowAddQuestion = ref(false)

  const onCancel = async () => {
    if (!isEqual(newQuestion.value, defaultNewQuestion)) {
      const agreed = await confirm({
        maxWidth: '380px',
        message: 'Form has unsaved changes. Are you sure you want to close it?',
        size: 'small',
      })
      if (agreed) {
        doShowAddQuestion.value = false
      }
    } else {
      doShowAddQuestion.value = false
    }
  }

  const onSave = async () => {
    if (form.validate()) {
      await commands.createQuestion({...newQuestion.value})
      doShowAddQuestion.value = false
    }
  }

  const showDialog = () => {
    newQuestion.value = { ...defaultNewQuestion }
    doShowAddQuestion.value = true
  }
</script>

<template>
  <div>
    <VaButton @click="showDialog">Add Question</VaButton>

    <VaModal
      v-model="doShowAddQuestion"
      size="small"
      mobile-fullscreen
      close-button
      hide-default-actions
    >
      <h1 class="va-h5">Create Question</h1>
      <VaForm v-slot="{ isValid }" ref="create-question-form" class="flex-col justify-start items-start gap-4 inline-flex w-full">
        <div class="self-stretch flex-col justify-start items-start gap-4 flex">
          <div class="flex gap-4 flex-col sm:flex-row w-full">
            <VaInput
              v-model="newQuestion.question"
              label="Question"
              class="w-full"
              :rules="[validators.required]"
              name="question"
            />
          </div>
          <div class="flex gap-4 flex-col sm:flex-row w-full">
            <VaInput
              v-model="newQuestion.answer"
              label="Answer"
              class="w-full"
              :rules="[validators.required]"
              name="answer"
            />
          </div>
          <div class="flex gap-4 flex-col sm:flex-row w-full">
            <VaTextarea
              v-model="newQuestion.hints"
              label="Hints"
              class="w-full"
              :rules="[validators.required]"
              name="hints"
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
