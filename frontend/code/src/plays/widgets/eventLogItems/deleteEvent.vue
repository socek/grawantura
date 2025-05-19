<script setup>
  import { useModal } from 'vuestic-ui'
  import commands from "@/plays/commands"

  const props = defineProps(['playId', 'eventId'])
  const { confirm } = useModal()

  const onDelete = async () => {
    const agreed = await confirm({
      maxWidth: '380px',
      message: `Are you sure you want to delete ${props.name} ?`,
      size: 'small',
    })
    if (agreed) {
      commands.deleteEvent(props.playId, props.eventId)
    }
  }

</script>

<template>
  <VaPopover message="Delete event">
    <VaButton
      color="danger"
      size="small"
      aria-label="Delete play"
      @click="onDelete()"
    >
      <VaIcon name="delete" />
    </VaButton>
  </VaPopover>
</template>
