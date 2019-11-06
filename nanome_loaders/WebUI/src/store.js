import Vue from 'vue'
import Vuex from 'vuex'
import API from '@/api'

Vue.use(Vuex)

const state = {
  token: localStorage.getItem('user-token') || null,
  unique: null,
  name: null
}

const mutations = {
  PATCH_USER(state, payload) {
    Object.assign(state, payload)
  }
}

async function saveSession(commit, { success, results }) {
  if (success) {
    const user = {
      unique: results.user.unique,
      name: results.user.name,
      token: results.token.value
    }
    commit('PATCH_USER', user)
    localStorage.setItem('user-token', results.token.value)

    try {
      await API.create('/' + results.user.unique)
    } catch (e) {}

    return true
  } else {
    localStorage.removeItem('user-token')
    return false
  }
}

const actions = {
  async login({ commit }, creds) {
    const data = await API.login(creds)
    return saveSession(commit, data)
  },

  async refresh({ commit }) {
    const data = await API.refresh()
    return saveSession(commit, data)
  },

  async logout({ commit }) {
    commit('PATCH_USER', {
      token: null,
      name: null,
      unique: null
    })
    localStorage.removeItem('user-token')
  }
}

export default new Vuex.Store({
  state,
  mutations,
  actions
})
