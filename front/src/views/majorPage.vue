<template>
  <div id="majorPage">
    <el-carousel
      :interval="1000"
      direction="horizontal"
      :autoplay="true"
      height="700px"
    >
      <el-carousel-item>
        <div class="carousel-item-content">
          <img src="../assets/selfDriving.png" class="backImg" />
          <div class="title-overlay">
            <p>混合交通流控制算法竞赛平台</p>
          </div>
        </div>
      </el-carousel-item>
      <el-carousel-item>
        <img src="../assets/lines.jpg" class="backImg" />
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
};
</script>
<style lang="scss" scoped>
.carousel-item-content {
  position: relative;
}

.title-overlay {
  position: absolute;
  top: 0px;
  left: 120px;
  width: 100%;
  color: white;
  padding: 20px;
  font-size: 36px; /* 调整字体大小 */
}

.backImg {
  width: 100%;
}
.outerBlock {
  padding: 30% 10%;
}
</style>
