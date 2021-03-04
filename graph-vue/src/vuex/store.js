import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
    clickPath: undefined,
    graphNetwork: undefined,
}
const mutations = {
    updateClickType(state, clickPath) {
        state.clickPath = clickPath
    },
    updateGraphNetwork(state, Network) {
        state.graphNetwork = Network
    }
}

export default new Vuex.Store({
    state,
    mutations
})