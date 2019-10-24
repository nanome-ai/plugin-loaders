import '@/assets/css/tailwind.css'
import Vue from 'vue'
import App from './App.vue'
import router from './router'

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

Vue.config.productionTip = false

Vue.directive('click-out', {
  bind(el, binding, vnode) {
    binding.stop = e => e.stopPropagation()
    binding.event = () => vnode.context[binding.expression]()

    document.body.addEventListener('click', binding.event)
    el.addEventListener('click', binding.stop)
  },
  unbind(el, binding) {
    document.body.removeEventListener('click', binding.event)
    el.removeEventListener('click', binding.stop)
  }
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
