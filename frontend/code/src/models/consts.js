export const Status = {
  BeforeLoad: 'BeforeLoad',
  Loading: 'Loading',
  Completed: 'Completed',
  Failed: 'Failed',
};

export const createDefaultState = (queryFn) => {
  return {
    namespaced: true,
    state: () => ({
      items: [],
      status: Status.BeforeLoad,
    }),
    getters: {
      getStatus (state) {
        return state.status
      },
      getItems (state) {
        return state.items
      }
    },
    mutations: {
      setStatus (state, status) {
        state.status = status
      },
      setItems (state, items) {
        state.items = items
      }
    },
    actions: {
      async fetch({ commit, state }, force) {
        force = force || false
        if (!force && state.status == Status.Completed) {
          return
        }
        await commit("setStatus", Status.Loading)
        try {
          const { data, error, status } = await queryFn()

          if (error && status !== 406) throw error

          if (data) {
            await commit("setItems", data)
            await commit("setStatus", Status.Completed)
          }
        } catch (error) {
          await commit("setStatus", Status.Failed)
          console.log(error)
        }
      }
    },
  }
}
