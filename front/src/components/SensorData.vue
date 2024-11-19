<template>
  <el-container class="container">
    <el-header>
      <h1>传感器数据</h1>
    </el-header>
    <el-main>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-card>
            <h2>温度</h2>
            <p>{{ temperature }} °C</p>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card>
            <h2>湿度</h2>
            <p>{{ humidity }} %</p>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card>
            <h2>土壤湿度值</h2>
            <p>{{ soilMoistureValue }}</p>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card>
            <h2>土壤湿度电压</h2>
            <p>{{ soilMoistureVoltage }} V</p>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
export default {
  name: 'SensorData',
  data() {
    return {
      temperature: '',
      humidity: '',
      soilMoistureValue: '',
      soilMoistureVoltage: ''
    }
  },
  created() {
    this.connectWebSocket();
  },
  methods: {
    connectWebSocket() {
      const ws = new WebSocket('ws://localhost:8000/ws');
      ws.onopen = () => {
        console.log('WebSocket connection opened');
      };
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('Received data:', data);
          const message = data.message;
          this.temperature = message.temperature;
          this.humidity = message.humidity;
          this.soilMoistureValue = message.soil_moisture_value;
          this.soilMoistureVoltage = message.soil_moisture_voltage;
        } catch (error) {
          console.error('Error parsing message:', error);
        }
      };
      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
      ws.onclose = () => {
        console.log('WebSocket connection closed');
      };
    }
  }
}
</script>

<style scoped>
h1, h2 {
  font-weight: normal;
}
</style>