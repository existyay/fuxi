<template>
  <div>
    <el-container>
      <el-header>
        <h1>传感器数据</h1>
      </el-header>
      <el-main>
        <el-card>
          <h2>传感器数据</h2>
          <el-row>
            <el-col :span="8">
              <el-card>
                <p>温度: {{ sensorData.temperature }}°C</p>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card>
                <p>湿度: {{ sensorData.humidity }}%</p>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card>
                <p>土壤湿度: {{ sensorData.soilMoisture }}%</p>
              </el-card>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              <el-card>
                <h2>图像</h2>
                <img :src="'data:image/jpeg;base64,' + sensorData.image" alt="传感器图像" />
              </el-card>
            </el-col>
          </el-row>
        </el-card>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  data () {
    return {
      sensorData: {
        temperature: '加载中...',
        humidity: '加载中...',
        soilMoisture: '加载中...',
        image: ''
      }
    }
  },
  mounted () {
    this.fetchSensorData()
  },
  methods: {
    async fetchSensorData () {
      const response = await fetch('/api/sensor_data')
      const data = await response.json()
      this.sensorData.temperature = data.temperature
      this.sensorData.humidity = data.humidity
      this.sensorData.soilMoisture = data.soil_moisture
      this.sensorData.image = data.image
    }
  }
}
</script>

<style scoped>
h1 {
  font-weight: normal;
}
</style>