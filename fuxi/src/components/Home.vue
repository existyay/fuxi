<template>
  <div>
    <h1>欢迎来到智慧农业系统</h1>
    <router-link to="/sensor-data">查看传感器数据</router-link>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
h1 {
  font-weight: normal;
}
</style>