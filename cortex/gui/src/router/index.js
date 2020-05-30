import Vue from 'vue'
import VueRouter from 'vue-router'
import Users from '../views/Users.vue'
import Snapshots from '../views/Snapshots.vue'
import Snapshot from '../views/Snapshot.vue'
import Topic from '../views/Topic.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Users',
    component: Users
  },
  {
    path: '/snapshots/:user_id',
    name: 'Snapshots',
    component: Snapshots,
    props: true
  },
  {
    path: '/snapshots/:user_id/:snapshot_id',
    name: 'Snapshot',
    component: Snapshot,
    props: true
  },
  {
    path: '/snapshots/:user_id/:snapshot_id/:topic',
    name: 'Topic',
    component: Topic,
    props: true
  }
]

const router = new VueRouter({
  routes
})

export default router
