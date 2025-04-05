<script setup>
  import { ref } from 'vue'
  import { validators } from '@/services/utils'
  import { useModal, useForm } from 'vuestic-ui'
  import { isEqual } from 'lodash';
  import useQuestionStore from '@/questions/store'
  import commands from "@/questions/commands"

  const props = defineProps(['gameId', 'itemId'])
  const questionStore = useQuestionStore(props.gameId)()
  const { confirm } = useModal()
  const form = useForm('edit-question-form')

  const isVisible = ref(false)

  const defaultQuestionData = () => {
    return questionStore.items.filter(item => {
      return item.id == props.itemId
    })[0]
  }

  const questionData = ref({ ...defaultQuestionData() })

  const onCancel = async () => {
    if (!isEqual(questionData.value, defaultQuestionData())) {
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
      await commands.editQuestion({
        "gameId": props.gameId,
        "questionId": props.itemId,
        "question": questionData.value.question,
        "answer": questionData.value.answer,
        "hints": questionData.value.hints,
      })
      isVisible.value = false
    }
  }

  const showDialog = () => {
    questionData.value = { ...defaultQuestionData() }
    isVisible.value = true
  }
</script>

<template>
  <div >
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
      <h1 class="va-h5">Edit Question</h1>
      <VaForm v-slot="{ isValid }" ref="edit-question-form" class="flex-col justify-start items-start gap-4 inline-flex w-full">
        <div class="self-stretch flex-col justify-start items-start gap-4 flex">
          <div class="flex gap-4 flex-col sm:flex-row w-full">
            <VaInput
              v-model="questionData.question"
              label="Question"
              class="w-full"
              :rules="[validators.required]"
              name="question"
            />
          </div>
          <div class="flex gap-4 flex-col sm:flex-row w-full">
            <VaInput
              v-model="questionData.answer"
              label="Answer"
              class="w-full"
              :rules="[validators.required]"
              name="answer"
            />
          </div>
          <div class="flex gap-4 flex-col sm:flex-row w-full">
            <VaTextarea
              v-model="questionData.hints"
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
