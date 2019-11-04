import '@/assets/css/tailwind.css'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Modal from '@/components/Modal'

Vue.config.productionTip = false

//#region fontawesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'

import {
  FontAwesomeIcon,
  FontAwesomeLayers,
  FontAwesomeLayersText
} from '@fortawesome/vue-fontawesome'

library.add(fas)
Vue.component('fa-icon', FontAwesomeIcon)
Vue.component('fa-layers', FontAwesomeLayers)
Vue.component('fa-text', FontAwesomeLayersText)
//#endregion

Vue.directive('click-out', {
  bind(el, binding, vnode) {
    binding.stop = e => e.stopPropagation()
    binding.event = () => vnode.context[binding.expression]()

    setTimeout(() => {
      document.body.addEventListener('click', binding.event)
      el.addEventListener('click', binding.stop)
    }, 0)
  },
  unbind(el, binding) {
    document.body.removeEventListener('click', binding.event)
    el.removeEventListener('click', binding.stop)
  }
})

store.dispatch('refresh')

const app = new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

// global modal singleton
const VModal = Vue.extend(Modal)
const modal = new VModal({ store })
modal.$mount()
Vue.prototype.$modal = modal
app.$root.$el.appendChild(modal.$el)
