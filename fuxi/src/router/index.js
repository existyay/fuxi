import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import SensorData from '@/components/SensorData'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/sensor-data',
      name: 'SensorData',
      component: SensorData
    }
  ]
})