import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
    clickPath: undefined,
    showMainGraph: false,
}
const mutations = {
    updateClickType(state, clickPath) {
        state.clickPath = clickPath
    },
    showMainGraph(state, isShowMainGraph) {
        state.showMainGraph = isShowMainGraph
    }

}

export default new Vuex.Store({
    state,
    mutations
})