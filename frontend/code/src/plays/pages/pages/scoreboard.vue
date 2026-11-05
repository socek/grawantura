<script setup>
import { computed, onMounted } from 'vue'

import useTeamStore from '@/teams/store'
import { useHostQuestionStore } from "@/plays/hoststore"
import { teamColor } from '@/plays/teamColors'

const props = defineProps(['playId'])
const questionStore = useHostQuestionStore(props.playId)()
const teamStore = useTeamStore(props.playId)()

onMounted(async () => {
  await teamStore.fetch()
  await questionStore.fetch()
})

const getMoney = (teamId) => {
  return questionStore.moneyPool[teamId] || 0
}

const getHints = (teamId) => {
  return questionStore.hints[teamId] || 0
}

// After the auction ends show the saved bids; during it, the live ones.
const isAuctionFinished = computed(() => Object.keys(questionStore.finalBids).length > 0)

const getAuctioned = (teamId) => {
  const bids = isAuctionFinished.value ? questionStore.finalBids : questionStore.auctionedPool
  return parseInt(bids[teamId]) || 0
}

// Teams ordered from the richest; the color stays tied to the team.
const rankedTeams = computed(() => {
  return teamStore.items
    .map((team) => ({
      id: team.id,
      name: team.name,
      money: getMoney(team.id),
      hints: getHints(team.id),
      auctioned: getAuctioned(team.id),
      color: teamColor(teamStore.items, team.id),
    }))
    .sort((a, b) => b.money - a.money)
})

const highestBid = computed(() => Math.max(0, ...rankedTeams.value.map((team) => team.auctioned)))

const formatMoney = (value) => value.toLocaleString('pl-PL')

</script>

<template>
  <div class="screen">
    <header class="top">
      <div class="pool">
        <span class="caption">Pula</span>
        <span class="pool-value">{{ formatMoney(getMoney("money_pool")) }}</span>
      </div>
    </header>

    <main class="teams">
      <div
        v-for="(team, index) in rankedTeams"
        :key="team.id"
        class="team"
        :style="{ '--team-color': team.color }"
      >
        <span class="place">{{ index + 1 }}</span>
        <span class="name">{{ team.name }}</span>
        <span class="stat hints">
          <span class="caption">Podpowiedzi</span>
          <span class="value">{{ team.hints }}</span>
        </span>
        <span
          class="stat auctioned"
          :class="{ leading: team.auctioned > 0 && team.auctioned == highestBid }"
        >
          <span class="caption">Zlicytowane</span>
          <span class="value">{{ formatMoney(team.auctioned) }}</span>
        </span>
        <span class="stat money">
          <span class="caption">Posiadane</span>
          <span class="value">{{ formatMoney(team.money) }}</span>
        </span>
      </div>
    </main>
  </div>
</template>

<style scoped>
.screen {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 3vh;
  padding: 3vh 4vw;
  box-sizing: border-box;
}

.caption {
  text-transform: uppercase;
  letter-spacing: 0.15em;
  font-weight: 700;
  font-size: clamp(0.8rem, 1.2vw, 1.3rem);
  opacity: 0.85;
}

.top {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: stretch;
  gap: 2vw;
}

.pool {
  display: flex;
  align-items: baseline;
  gap: 2vw;
  padding: 1.25vh 3vw;
  border-radius: 1.75rem;
  background: linear-gradient(135deg, #facc15, #f59e0b);
  color: #1e1b4b;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
}
.pool-value {
  font-weight: 800;
  font-size: clamp(1.75rem, 4vw, 4.25rem);
  font-variant-numeric: tabular-nums;
}

.teams {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 2vh;
}

.team {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 2vw;
  padding: 2vh 2.5vw;
  border-radius: 1.5rem;
  background: rgba(255, 255, 255, 0.08);
  border-left: 1rem solid var(--team-color);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.place {
  flex: none;
  width: clamp(2.5rem, 5vw, 5rem);
  height: clamp(2.5rem, 5vw, 5rem);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--team-color);
  font-weight: 800;
  font-size: clamp(1.25rem, 2.5vw, 2.5rem);
}

.name {
  flex: 1 1 12rem;
  font-weight: 800;
  font-size: clamp(1.5rem, 3.5vw, 3.75rem);
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5vh;
}
.stat .caption {
  line-height: 1.2;
}
.stat .value {
  font-weight: 800;
  font-variant-numeric: tabular-nums;
  line-height: 1.1;
}
.hints .value {
  font-size: clamp(1.25rem, 2.5vw, 2.75rem);
}
.auctioned {
  min-width: 10vw;
  padding: 0.5vh 1vw;
  border-radius: 1rem;
}
.auctioned .value {
  font-size: clamp(1.5rem, 3.5vw, 3.75rem);
}
.auctioned.leading {
  background: var(--team-color);
}
.money .value {
  font-size: clamp(1.5rem, 3.5vw, 3.75rem);
  color: #facc15;
}
</style>
