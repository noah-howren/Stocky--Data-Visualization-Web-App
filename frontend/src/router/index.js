import Home from '../views/Home.vue'
import Stocks from '../views/Stocks.vue'
import Crypto from '../views/Crypto.vue'
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
      path:'/',
      redirect: '/Stocks'
    },
    {
      path:'/Stocks/:Ticker',
      component: Stocks
    },
    {
      path:'/Stocks',
      component: Home
    },
    {
      path:'/Crypto',
      component: Home
    },
    {
      path:'/Crypto/:Ticker',
      component: Crypto
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