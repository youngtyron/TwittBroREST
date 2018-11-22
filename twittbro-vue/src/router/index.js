import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home.vue'
import Login from '@/components/Login.vue'
import Registration from '@/components/Registration.vue'
import MyWall from '@/components/MyWall.vue'
import Wall from '@/components/Wall.vue'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/registration',
      name: 'registration',
      component: Registration
    },
    {
      path: '/mywall',
      name: 'mywall',
      component: MyWall
    },
    {
      path: '/wall/:id',
      name: 'wall',
      component: Wall
    },
  ]
})
