<template>
  <el-container class="container">
    <el-header>
      <h1>本地天气信息</h1>
    </el-header>
    <el-main>
      <el-row :gutter="10">
        <el-col :span="24">
          <el-card>
            <h2>实时天气</h2>
            <p>温度: {{ weather.temperature }} °C</p>
            <p>湿度: {{ weather.humidity }} %</p>
            <p>天气: {{ weather.weather }} </p>
            <p>风向: {{ weather.windDirection }} </p>
            <p>风力: {{ weather.windPower }} 级</p>
            <p>更新时间: {{ weather.reportTime }} </p>
          </el-card>
        </el-col>
      </el-row>
      <el-row :gutter="10" style="margin-top: 20px;">
        <el-col :span="24">
          <el-card>
            <h2>未来4天天气预报</h2>
            <p v-for="forecast in forecasts" :key="forecast.date">
              {{ forecast.date }} - {{ forecast.dayWeather }} - {{ forecast.nightTemp }}~{{ forecast.dayTemp }}℃
            </p>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LocateWeather',
  data() {
    return {
      weather: {
        temperature: '',
        humidity: '',
        weather: '',
        windDirection: '',
        windPower: '',
        reportTime: ''
      },
      forecasts: []
    }
  },
  mounted() {
    this.loadWeather();
  },
  methods: {
    async loadWeather() {
      const apiKey = 'd1f40f7e6ae6613faf15b9c2c4127698'; // 替换为你的高德地图 API 密钥
      const cityCode = '330100'; // 替换为你要查询的城市编码

      try {
        // 获取实时天气信息
        const liveResponse = await axios.get(`https://restapi.amap.com/v3/weather/weatherInfo`, {
          params: {
            key: apiKey,
            city: cityCode,
            extensions: 'base',
            output: 'JSON'
          }
        });

        if (liveResponse.data.status === '1') {
          const liveData = liveResponse.data.lives[0];
          this.weather = {
            temperature: liveData.temperature,
            humidity: liveData.humidity,
            weather: liveData.weather,
            windDirection: liveData.winddirection,
            windPower: liveData.windpower,
            reportTime: liveData.reporttime
          };
        } else {
          console.error('获取实时天气数据失败:', liveResponse.data.info);
        }

        // 获取未来4天天气预报
        const forecastResponse = await axios.get(`https://restapi.amap.com/v3/weather/weatherInfo`, {
          params: {
            key: apiKey,
            city: cityCode,
            extensions: 'all',
            output: 'JSON'
          }
        });

        if (forecastResponse.data.status === '1') {
          this.forecasts = forecastResponse.data.forecasts[0].casts.map(forecast => ({
            date: forecast.date,
            dayWeather: forecast.dayweather,
            nightTemp: forecast.nighttemp,
            dayTemp: forecast.daytemp
          }));
        } else {
          console.error('获取天气预报数据失败:', forecastResponse.data.info);
        }
      } catch (error) {
        console.error('请求天气数据失败:', error);
      }
    }
  }
}
</script>

<style scoped>
h1 {
  font-weight: normal;
}
</style>