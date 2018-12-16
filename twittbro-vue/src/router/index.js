import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home.vue'
import Login from '@/components/Login.vue'
import Registration from '@/components/Registration.vue'
import MyWall from '@/components/MyWall.vue'
import Wall from '@/components/Wall.vue'
import News from '@/components/News.vue'
import Search from '@/components/Search.vue'
import Follows from '@/components/Follows.vue'
import Messenger from '@/components/Messenger.vue'
import Dialogue from '@/components/Dialogue.vue'


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
    {
      path: '/news',
      name: 'news',
      component: News
    },
    {
      path: '/search',
      name: 'search',
      component: Search
    },
    {
      path: '/follows',
      name: 'follows',
      component: Follows
    },
    {
      path: '/messenger',
      name: 'messenger',
      component: Messenger
    },
    {
      path: '/dialogue/:id',
      name: 'dialogue',
      component: Dialogue
    },
  ]
})
