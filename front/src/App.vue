<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import SensorData from './components/SensorData.vue'
import MediaDisplay from './components/MediaDisplay.vue'

export default {
  name: 'App',
  components: {
    SensorData,
    MediaDisplay
  }
}
</script>

<style>
#app {
  font-family: Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>