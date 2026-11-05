<script setup>
import { computed, onMounted } from 'vue'

import useTeamStore from '@/teams/store'
import { useHostQuestionStore } from "@/plays/hoststore"
import { teamColor } from '@/plays/teamColors'

// Read-only game history for the game screen. Shows the same information
// as the host's history (@/plays/widgets/eventsLog.vue), without buttons.
const props = defineProps(['playId'])
const questionStore = useHostQuestionStore(props.playId)()
const teamStore = useTeamStore(props.playId)()

onMounted(async () => {
  await teamStore.fetch()
  await questionStore.fetch()
})

const SHOWN_EVENTS = ['init money', 'question draw', 'end auction', 'hint', 'answer']

// Events grouped into rounds: every drawn question starts a new round.
const rounds = computed(() => {
  const result = []
  let current = null
  for (const event of questionStore.events || []) {
    if (!SHOWN_EVENTS.includes(event.typename)) {
      continue
    }
    if (event.typename == 'question draw' || current === null) {
      current = { id: event.id, events: [] }
      result.push(current)
    }
    current.events.push(event)
  }
  return result
})

const teamName = (teamId) => {
  const team = teamStore.getItemById(teamId)
  return team ? team.name : ''
}

const colorOf = (teamId) => teamColor(teamStore.items, teamId)

const formatMoney = (value) => (parseInt(value) || 0).toLocaleString('pl-PL')

// --- end auction ---
const auctionBids = (event) => {
  const bids = { ...event.payload }
  delete bids.addon
  return bids
}

const auctionWinner = (event) => {
  let winner = null
  let highest = 0
  for (const [teamId, value] of Object.entries(auctionBids(event))) {
    if (value > highest) {
      highest = value
      winner = teamId
    }
  }
  return winner
}

const auctionSum = (event) => {
  let sum = event.money_stamp || 0
  for (const value of Object.values(event.payload)) {
    sum += parseInt(value) || 0
  }
  return sum
}

// --- hint ---
// Teams whose money changed or who bought/used a hint, like in the host's log.
const hintTeams = (event) => {
  const result = {}
  for (const [teamId, value] of Object.entries(event.payload.money || {})) {
    if (value != 0) {
      result[teamId] = value
    }
  }
  for (const teamId of Object.keys(event.payload.change || {})) {
    result[teamId] = result[teamId] || 0
  }
  return result
}

const hintChange = (event, teamId) => {
  const change = (event.payload.change || {})[teamId] || 0
  if (change > 0) return 'bought'
  if (change < 0) return 'used'
  return ''
}
</script>

<template>
  <div class="screen">
    <h1 class="title">Historia</h1>

    <div class="scroller">
      <div class="rounds" v-if="rounds.length">
        <section v-for="round in rounds" :key="round.id" class="round">
          <template v-for="event in round.events" :key="event.id">

            <div v-if="event.typename == 'init money'" class="entry">
              <p class="entry-title">Początek gry</p>
              <div class="chips">
                <span
                  v-for="(value, teamId) in event.payload"
                  :key="teamId"
                  class="chip"
                  :style="{ '--team-color': colorOf(teamId) }"
                >{{ teamName(teamId) }}: {{ formatMoney(value) }}</span>
              </div>
            </div>

            <div v-else-if="event.typename == 'question draw'" class="entry">
              <p class="entry-title">Wylosowano pytanie</p>
              <p class="question">{{ event.question_text }}</p>
            </div>

            <div v-else-if="event.typename == 'end auction'" class="entry">
              <p class="entry-title">Licytacja</p>
              <div class="chips">
                <span class="chip neutral">Pula przed: {{ formatMoney(event.money_stamp) }}</span>
                <span class="chip neutral">Dodatek: {{ formatMoney(event.payload.addon) }}</span>
                <span class="chip neutral">Suma: {{ formatMoney(auctionSum(event)) }}</span>
                <span
                  v-for="(value, teamId) in auctionBids(event)"
                  :key="teamId"
                  class="chip"
                  :class="{ winner: auctionWinner(event) == teamId }"
                  :style="{ '--team-color': colorOf(teamId) }"
                >{{ teamName(teamId) }}: {{ formatMoney(value) }}</span>
              </div>
            </div>

            <div v-else-if="event.typename == 'hint'" class="entry">
              <p class="entry-title">Podpowiedź</p>
              <div class="chips">
                <span
                  v-for="(value, teamId) in hintTeams(event)"
                  :key="teamId"
                  class="chip"
                  :class="hintChange(event, teamId)"
                  :style="{ '--team-color': colorOf(teamId) }"
                >
                  {{ teamName(teamId) }}: {{ formatMoney(value) }}
                  <span v-if="hintChange(event, teamId) == 'bought'">(kupiona)</span>
                  <span v-if="hintChange(event, teamId) == 'used'">(użyta)</span>
                </span>
              </div>
            </div>

            <div
              v-else-if="event.typename == 'answer'"
              class="entry answer"
              :class="event.payload.success ? 'correct' : 'wrong'"
            >
              <p class="entry-title">{{ event.payload.success ? 'Dobra odpowiedź' : 'Zła odpowiedź' }}</p>
            </div>

          </template>
        </section>
      </div>
      <p v-else class="empty">Brak wydarzeń</p>
    </div>
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

.title {
  font-weight: 800;
  font-size: clamp(1.75rem, 4vw, 4rem);
  text-align: center;
}

/* column-reverse keeps the view scrolled to the newest events. */
.scroller {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  display: flex;
  flex-direction: column-reverse;
}

.rounds {
  display: flex;
  flex-direction: column;
  gap: 2vh;
}

.round {
  display: flex;
  flex-direction: column;
  gap: 1.25vh;
  padding: 2vh 2vw;
  border-radius: 1.5rem;
  background: rgba(255, 255, 255, 0.08);
  border: 2px solid rgba(255, 255, 255, 0.12);
}

.entry-title {
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 700;
  font-size: clamp(0.8rem, 1.2vw, 1.3rem);
  opacity: 0.85;
  margin-bottom: 0.75vh;
}

.question {
  font-weight: 700;
  font-size: clamp(1.1rem, 2.2vw, 2.25rem);
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75vw;
}

.chip {
  display: inline-flex;
  gap: 0.5vw;
  align-items: baseline;
  padding: 0.6vh 1vw;
  border-radius: 999px;
  font-weight: 700;
  font-size: clamp(0.9rem, 1.5vw, 1.6rem);
  font-variant-numeric: tabular-nums;
  background: rgba(255, 255, 255, 0.1);
  border-left: 0.5rem solid var(--team-color, transparent);
}
.chip.neutral {
  background: rgba(15, 23, 42, 0.6);
}
.chip.winner {
  background: var(--team-color);
}
.chip.bought {
  background: linear-gradient(135deg, #22c55e, #15803d);
}
.chip.used {
  background: linear-gradient(135deg, #facc15, #f59e0b);
  color: #1e1b4b;
}

.entry.answer {
  align-self: flex-start;
  padding: 0.75vh 1.5vw;
  border-radius: 1rem;
}
.entry.answer .entry-title {
  margin: 0;
  opacity: 1;
  font-size: clamp(1rem, 1.8vw, 2rem);
}
.answer.correct {
  background: linear-gradient(135deg, #22c55e, #15803d);
}
.answer.wrong {
  background: linear-gradient(135deg, #ef4444, #b91c1c);
}

.empty {
  text-align: center;
  font-size: clamp(1.25rem, 2.5vw, 2.5rem);
  opacity: 0.7;
}
</style>
