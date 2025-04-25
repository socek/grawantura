<script setup>
  import { useModal } from 'vuestic-ui'
  import commands from "@/teams/commands"

  const props = defineProps(['playId', 'itemId', 'name'])
  const { confirm } = useModal()

  const onDelete = async () => {
    const agreed = await confirm({
      maxWidth: '380px',
      message: `Are you sure you want to delete ${props.name} ?`,
      size: 'small',
    })
    if (agreed) {
      await commands.deleteTeam(props.playId, props.itemId)
    }
  }
</script>

<template>
  <div class="flex gap-2 justify-end">
    <VaPopover message="Delete play">
      <VaButton
        color="danger"
        size="small"
        aria-label="Delete play"
        @click="onDelete()"
      >
        <VaIcon name="delete" />
      </VaButton>
    </VaPopover>
  </div>
</template>
