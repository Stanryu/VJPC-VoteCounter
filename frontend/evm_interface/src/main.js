import Vue from 'vue'
import App from './App.vue'
import router from './router'

// Need to install it first => npm install bootstrap@4.6.0 --save
import 'bootstrap/dist/css/bootstrap.css'
import BootstrapVue from 'bootstrap-vue';

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import { faCheckCircle } from '@fortawesome/free-solid-svg-icons'
import { faExclamationCircle } from '@fortawesome/free-solid-svg-icons'

/* add icons to the library */
library.add(faCheckCircle, faExclamationCircle)

/* add font awesome icon component */
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.productionTip = false
Vue.use(BootstrapVue)

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
