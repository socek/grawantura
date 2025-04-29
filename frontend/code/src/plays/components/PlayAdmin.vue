<script setup>
  import commands from "@/plays/commands"

  const props = defineProps(['playId'])

  const drawQuestion = async () => {
    await commands.drawQuestion(props.playId)
  }
</script>

<template>
  <VaCard>
    <VaCardTitle>Licytacja</VaCardTitle>
    <VaCardActions align="stretch" vertical>
      <VaButton color="success" @click="drawQuestion">Losuj Pytanie</VaButton>
      <VaButton>Scorboard</VaButton>
      <VaButton>Pytanie</VaButton>
    </VaCardActions>
    <!-- <VaCardContent>
      <div class="flex flex-col md:flex-row gap-2 mb-2">
        Odpowiedź
      </div>
      <div class="flex flex-col md:flex-row gap-2 mb-2">
        <VaButton color="success">Dobra Odpowiedź</VaButton>
        <VaButton color="danger">Zła Odpowiedź</VaButton>
        <VaButton color="warning">Pokaż podpowiedź</VaButton>
      </div>
      <div class="flex flex-col md:flex-row gap-2 mb-2">
        Timer
      </div>
      <div class="flex flex-col md:flex-row gap-2 mb-2">
        <VaButton color="success">Start</VaButton>
        <VaButton color="danger">Stop</VaButton>
        <VaButton color="warning">Reset</VaButton>
      </div>
    </VaCardContent> -->
  </VaCard>
</template>
