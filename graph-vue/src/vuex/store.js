import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
    clickPath: undefined,
}
const mutations = {
    updateClickType(state, clickPath) {
        state.clickPath = clickPath
    }
}

export default new Vuex.Store({
    state,
    mutations
})