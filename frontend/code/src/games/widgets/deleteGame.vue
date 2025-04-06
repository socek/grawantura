<script setup>
  import { useModal } from 'vuestic-ui'
  import commands from '@/games/commands'

  const props = defineProps(['item_id', 'name'])
  const { confirm } = useModal()


  const onDelete = async () => {
    const agreed = await confirm({
      maxWidth: '380px',
      message: `Are you sure you want to delete ${props.name} ?`,
      size: 'small',
    })
    if (agreed) {
      await commands.deleteGame(props.item_id)
    }
  }
</script>

<template>
  <div class="flex gap-2 justify-end">
    <VaButton
      preset="primary"
      size="small"
      icon="mso-delete"
      aria-label="Delete user"
      @click="onDelete()"
    />
  </div>
</template>
