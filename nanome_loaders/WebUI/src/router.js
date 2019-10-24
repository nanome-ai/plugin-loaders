import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/*',
      name: 'home',
      component: Home
    }
  ]
})

router.beforeEach((to, from, next) => {
  let path = to.path.replace(/\/\/+/g, '/')

  if (path.slice(-1) !== '/') {
    path += '/'
  }

  if (path !== to.path) {
    next({ path, replace: true })
  }

  next()
})

export default router
