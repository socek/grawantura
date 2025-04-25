<script setup>
  import { useModal } from 'vuestic-ui'
  import commands from "@/questions/commands"

  const props = defineProps(['gameId', 'itemId', 'question'])
  const { confirm } = useModal()

  const onDelete = async () => {
    const agreed = await confirm({
      maxWidth: '380px',
      message: `Are you sure you want to delete ${props.question} ?`,
      size: 'small',
    })
    if (agreed) {
      await commands.deleteQuestion(props.gameId, props.itemId)
    }
  }
</script>

<template>
  <div class="flex gap-2 justify-end">
    <VaPopover message="Delete user">
      <VaButton
        color="danger"
        size="small"
        aria-label="Delete user"
        @click="onDelete()"
      >
        <VaIcon name="delete" />
      </VaButton>
    </VaPopover>
  </div>
</template>
