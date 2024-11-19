<template>
  <el-container class="container media-display">
    <el-header>
      <h2>实时图片</h2>
    </el-header>
    <el-main>
      <el-image :src="imageUrl" alt="实时图片" style="width: 100%;"></el-image>
      <el-button type="primary" @click="captureImage" style="margin-top: 20px;">拍摄</el-button>
      <h2>实时视频</h2>
      <video ref="videoPlayer" :src="videoUrl" controls autoplay style="width: 100%;"></video>
    </el-main>
  </el-container>
</template>

<script>
export default {
  name: 'MediaDisplay',
  data() {
    return {
      imageUrl: 'http://222.186.21.66:6888/capture',
      videoUrl: 'http://222.186.21.66:6889/stream'
    };
  },
  mounted() {
    this.$refs.videoPlayer.addEventListener('error', this.handleVideoError);
    this.loadAndPlayVideo();
  },
  beforeDestroy() {
    this.$refs.videoPlayer.removeEventListener('error', this.handleVideoError);
  },
  methods: {
    loadAndPlayVideo() {
      const video = this.$refs.videoPlayer;
      console.log('Loading video from URL:', this.videoUrl);
      video.load();
      video.play().catch(error => {
        console.error('视频播放错误:', error);
        alert('视频播放失败，请检查视频源 URL 或格式是否正确。');
      });
    },
    handleVideoError(event) {
      console.error('视频加载错误:', event);
      alert('视频加载失败，请检查视频源 URL 或格式是否正确。');
    },
    captureImage() {
      // 发送请求以获取最新的图像
      this.imageUrl = `http://222.186.21.66:6888/capture?timestamp=${new Date().getTime()}`;
    }
  }
}
</script>

<style scoped>
.media-display {
  text-align: center;
}

.media-display img, .media-display video {
  max-width: 100%;
  height: auto;
}
</style>