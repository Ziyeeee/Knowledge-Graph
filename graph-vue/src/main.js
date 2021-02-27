import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios';
import VueAxios from 'vue-axios';
import store from './vuex/store'

Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.use(VueAxios, axios)

new Vue({
  store,
  render: h => h(App),
}).$mount('#app')