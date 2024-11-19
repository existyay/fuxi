import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import SensorData from '@/components/SensorData'
import MediaDisplay from '@/components/MediaDisplay'
import LocateWeather from '@/components/LocateWeather'

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
    },
    {
      path: '/media-display',
      name: 'MediaDisplay',
      component: MediaDisplay
    },
    {
      path: '/locate-weather',
      name: 'LocateWeather',
      component: LocateWeather
    }
  ]
})