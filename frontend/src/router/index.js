import Home from '../views/Home.vue'
import Ticker from '../views/Ticker.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  
  routes: [
    {
      path:'/',
      redirect: '/Stocks'
    },
    {
      path:'/Stocks/:Ticker',
      component: Ticker
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
      component: Ticker
    }
  ]
})


export default router