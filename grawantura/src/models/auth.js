import { supabase } from './supabase'

export default {
    namespaced: true,
    state: () => ({
      initialized: false,
      isAuthenticated: false,
      session: null,
    }),
    getters: {
      isAuthenticated (state) {
        return state.isAuthenticated
      },
      getSession (state) {
        return state.session
      },
    },
    mutations: {
      setInitialized (state, initialized) {
        state.initialized = initialized
      },
      setSession (state, session) {
        console.log("ss", session, session ? true : false)
        state.session = session
        state.isAuthenticated = session ? true : false
      }
    },
    actions: {
      async init({ commit, state }) {
        if (state.initialized) {
          return
        }

        supabase.auth.getSession().then(({ data }) => {
          commit("setSession", data.session)
        })

        supabase.auth.onAuthStateChange((_, _session) => {
          commit("setSession", _session)
        })
      },
    }
}
