<template>
  <el-container class="container">
    <el-header>
      <h1>欢迎来到智慧农业系统</h1>
    </el-header>
    <el-main>
      <el-row :gutter="10">
        <el-col :span="8">
          <router-link to="/sensor-data">
            <el-button type="primary" size="large" block>查看传感器数据</el-button>
          </router-link>
        </el-col>
        <el-col :span="8">
          <router-link to="/media-display">
            <el-button type="success" size="large" block>查看监控</el-button>
          </router-link>
        </el-col>
        <el-col :span="8">
          <router-link to="/locate-weather">
            <el-button type="info" size="large" block>查看本地天气</el-button>
          </router-link>
        </el-col>
      </el-row>
      <el-row :gutter="10" style="margin-top: 20px;">
        <el-col :span="24">
          <el-card>
            <h2>近期传感器数据</h2>
            <el-table :data="recentData" style="width: 100%">
              <el-table-column prop="topic" label="主题" width="180"></el-table-column>
              <el-table-column prop="message" label="消息" :formatter="formatMessage"></el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      recentData: []
    }
  },
  created() {
    this.fetchRecentData();
  },
  methods: {
    async fetchRecentData() {
      try {
        const response = await this.$axios.get('/recent-data');
        this.recentData = response.data;
      } catch (error) {
        console.error('获取近期数据失败:', error);
      }
    },
    formatMessage(row, column, cellValue) {
      return JSON.stringify(cellValue);
    }
  }
}
</script>

<style scoped>
h1 {
  font-weight: normal;
}
</style>