import Test from '../components/default_vue/Test.vue'
import Home from '../views/Home/Home.vue'
import Stocks from '../views/Stocks.vue'

import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  
  routes: [
    //{
    //  path: '/',
    //  name: 'home',
    //  component: HomeView
    //},
    {
      path:'/Test',
      name: 'Test',
      component: Test
    },
    {
      path:'/',
      name: 'Home',
      component: Home
    },
    {
      path:'/Stocks/:Ticker',
      component: Stocks
    }
    //{
      //path: '/about',
      //name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      //component: () => import('../views/AboutView.vue')
    //}
  ]
})

export default router