import Vue from 'vue'
import App from './App.vue'
import router from './router'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import JQuery from 'jquery'
let $ = JQuery



// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)


Vue.config.productionTip = false

var api_url = $("#url_elem").val(); 
Vue.mixin({
  data: function() {
    return {
      get hostUrl() {
        return api_url;
        // if(api_url){
        //     return api_url
        // } else {
        //     console.log("Didn't get api URL from HTML")
        //     return "http://localhost:5000"
        // };
      }
    }
  }
})



new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
