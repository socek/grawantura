<script setup>
  import { computed, onMounted } from 'vue'
  import { Status } from '@/base/basestore'
  import { useHostQuestionStore } from "@/plays/hoststore"
  import useTeamStore from '@/teams/store'
  import { teamColor } from '@/plays/teamColors'
  import PlayTimer from "@/plays/components/PlayTimer.vue"

  const props = defineProps(['playId'])
  const teamStore = useTeamStore(props.playId)()
  const questionStore = useHostQuestionStore(props.playId)()

  // answerStatus: 0 - no answer yet, 1 - correct, 2 - wrong
  const isAnswerVisible = computed(() => questionStore.answerStatus > 0)
  const isAnswerCorrect = computed(() => questionStore.answerStatus == 1)
  const isHintsVisible = computed(() => questionStore.showHint)

  onMounted(async () => {
    await questionStore.fetch()
    await teamStore.fetch()
  })

  const isLoading = computed(() => {
    return [Status.BeforeLoad, Status.Loading].indexOf(questionStore.status) != -1
  })

  const answeringTeam = computed(() => {
    if (questionStore.answeringTeamId) {
      return teamStore.getItemById(questionStore.answeringTeamId)
    }
    return null
  })

  const answeringTeamColor = computed(() => {
    return teamColor(teamStore.items, questionStore.answeringTeamId)
  })

</script>

<template>
  <div v-if="!isLoading && questionStore.question" class="screen">
    <header class="top-bar">
      <div class="team-badge" v-if="answeringTeam" :style="{ background: answeringTeamColor }">
        <span class="label">Odpowiada</span>
        <span class="name">{{ answeringTeam.name }}</span>
      </div>
      <div class="team-badge waiting" v-else>
        <span class="label">Licytacja</span>
      </div>
      <PlayTimer :playId="props.playId" />
    </header>

    <main class="question-area">
      <p class="caption">Pytanie</p>
      <p class="question">{{ questionStore.question.question }}</p>
    </main>

    <footer class="bottom-area" v-if="isHintsVisible || isAnswerVisible">
      <section class="panel hints" v-if="isHintsVisible">
        <p class="caption">Podpowiedzi</p>
        <p class="hints-text">{{ questionStore.question.hints }}</p>
      </section>
      <section
        class="panel answer"
        :class="isAnswerCorrect ? 'correct' : 'wrong'"
        v-if="isAnswerVisible"
      >
        <p class="caption">{{ isAnswerCorrect ? 'Dobra odpowiedź!' : 'Zła odpowiedź' }}</p>
        <p class="answer-text">{{ questionStore.question.answer }}</p>
      </section>
    </footer>
  </div>
</template>

<style scoped>
  .screen {
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 2vh;
    padding: 3vh 4vw;
    box-sizing: border-box;
  }

  .caption {
    text-transform: uppercase;
    letter-spacing: 0.15em;
    font-weight: 700;
    font-size: clamp(0.9rem, 1.4vw, 1.4rem);
    opacity: 0.8;
    margin-bottom: 1vh;
  }

  .top-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 2vw;
    align-items: stretch;
    justify-content: space-between;
  }

  .team-badge {
    display: flex;
    align-items: baseline;
    gap: 1.5vw;
    padding: 1.5vh 2.5vw;
    border-radius: 1.5rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
  }
  .team-badge.waiting {
    background: rgba(255, 255, 255, 0.12);
  }
  .team-badge .label {
    text-transform: uppercase;
    letter-spacing: 0.15em;
    font-weight: 700;
    font-size: clamp(0.9rem, 1.4vw, 1.4rem);
  }
  .team-badge .name {
    font-weight: 800;
    font-size: clamp(1.5rem, 3.5vw, 3.5rem);
  }

  .question-area {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
    padding: 3vh 4vw;
    border-radius: 2rem;
    background: rgba(255, 255, 255, 0.08);
    border: 2px solid rgba(255, 255, 255, 0.15);
  }
  .question {
    font-weight: 700;
    line-height: 1.25;
    font-size: clamp(1.75rem, 4.5vw, 5rem);
  }

  .bottom-area {
    display: flex;
    flex-wrap: wrap;
    gap: 2vw;
  }
  .panel {
    flex: 1 1 30rem;
    padding: 2vh 2.5vw;
    border-radius: 1.5rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
  }
  .hints {
    background: linear-gradient(135deg, #f59e0b, #d97706);
  }
  .hints-text {
    white-space: pre-wrap;
    font-weight: 600;
    font-size: clamp(1.1rem, 2.2vw, 2.4rem);
    line-height: 1.35;
  }
  .answer.correct {
    background: linear-gradient(135deg, #22c55e, #15803d);
  }
  .answer.wrong {
    background: linear-gradient(135deg, #ef4444, #b91c1c);
  }
  .answer-text {
    font-weight: 800;
    font-size: clamp(1.5rem, 3.5vw, 4rem);
  }
</style>
