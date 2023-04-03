import Vue from 'vue'
import VueRouter from 'vue-router'
import ConfigElection from '../components/ConfigElection.vue'
import ElectoralVoting from '../components/ElectoralVoting.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'config',
    component: ConfigElection
  },
  {
    path: '/totalization',
    name: 'totalization',
    // route level code-splitting
    // this generates a separate chunk (totalization.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "totalization" */ '../components/ElectionTotalization.vue')
  },
  {
    path: '/voting',
    name: 'voting',
    component: ElectoralVoting
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
