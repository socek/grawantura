import { defineStore } from "pinia"

export const Status = {
  BeforeLoad: 'BeforeLoad',
  Loading: 'Loading',
  Completed: 'Completed',
  Failed: 'Failed',
}

export const createDefaultState = (name, queryFn) => {
  return defineStore(name, {
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
    actions: {
      setStatus (status) {
        this.status = status
      },
      setItems (items) {
        this.items = items
      },
      async fetch(force) {
        force = force || false
        if (!force && this.status == Status.Completed) {
          return
        }
        this.setStatus(Status.Loading)
        try {
          const { data, error, status } = await queryFn()

          if (error && status !== 406) throw error

          if (data) {
            this.setItems(data.items)
            this.setStatus(Status.Completed)
          }
        } catch (error) {
          this.setStatus(Status.Failed)
          console.log(error)
        }
      }

    }
  })
}
