import Vue from 'vue'
import App from './App.vue'
import router from './router'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'


// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)


Vue.config.productionTip = false

Vue.mixin({
  data: function() {
    return {
      get hostUrl() {
        return "http://localhost:5000";
      }
    }
  }
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')