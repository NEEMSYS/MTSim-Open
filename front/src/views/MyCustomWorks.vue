<template>
  <div id="works">
    <div class="content">
      <div style="display: grid; min-height: 697px; width: 100%">
        <div class="second">
          <div class="asside">
            <div class="menu">
              <div class="top">
                <div class="head">
                  <img
                    src="https://www.onsite.com.cn/assets/head.3c2902c3.png"
                  />
                </div>
                <div class="name">
                  <div class="content">{{ getUser.username }}</div>
                </div>
              </div>
              <el-menu default-active="2" class="el-menu-vertical-demo">
                  <el-menu-item index="1">
                    <i class="el-icon-trophy"></i>
                    <a href="MyGame">我的比赛</a>
                  </el-menu-item>
                  <el-menu-item index="2">
                    <i class="el-icon-trophy"></i>
                    <a href="works">作品管理</a>
                  </el-menu-item>
                  <el-menu-item index="3">
                    <i class="el-icon-trophy"></i>
                    <a href="MyCustomWorks">自定义场景</a>
                  </el-menu-item>
                </el-menu>
            </div>
          </div>
          <div class="right">
            <div class="works">
              <div class="title">自定义场景测试记录</div>
              <div class="table">
                <el-table
                  :data="gameData"
                  :header-cell-style="head_style"
                  style="width: 100%"
                >
                  <el-table-column
                    prop="competition_name"
                    label="比赛名称"
                    align="center"
                  >
                  </el-table-column>
                  
                  <el-table-column
                    prop="scenario_type"
                    label="场景类型"
                    align="center"
                  >
                  </el-table-column>

                  <el-table-column
                    prop="add_time"
                    label="上传时间"
                    align="center"
                  >
                  </el-table-column>
                  <el-table-column prop="score" label="分数" align="center">
                  </el-table-column>

                  <el-table-column
                    prop="result_file"
                    label="测评结果下载"
                    align="center">
                    <template slot-scope="scope">
                      <el-button type="primary" @click="download(scope.row.result_file)">结果下载</el-button>
          
                     </template>
                     <!-- <el-button type="primary" @click="download(result_file)">结果下载</el-button> -->
                    
                  </el-table-column>
                </el-table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      islogin: false,
      gameData: [],
    };
  },
  computed: {
    getUser() {
      return this.$store.state.user;
    },
  },
  created() {
    this.MySubmit();
  },
  methods: {

      //下载信息
      download(fileUrl) {
        // 校验参数
      if (!fileUrl) {
      this.$message.error('下载链接无效！'); // 使用 ElementUI 等 UI 库提示
      return;
    }
        // 移除URL中可能包含的重复域名部分
        const cleanUrl = fileUrl.replace('http://114.215.195.207', '');
        // 拼接正确的下载地址
        window.location.href = `http://114.215.195.207:8000${cleanUrl}`;
      },
    // 跳转到排行榜页面
    pushgrade() {
      this.$router.push("grade");
    },

    MySubmit() {
      const username = this.$store.state.user.username;
      axios
        .get(`api/userWorks/?username=${username}`)
        .then((res) => {
          this.gameData = res.data;
        });
    },
    head_style({ row, column, rowIndex, columnIndex }) {
      if (rowIndex === 0) {
        return {
          background: "rgb(232, 245, 255)",
          "text-align": "center",
        };
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.content {
  width: 100%;
  flex: 1;
}

.content .second {
  width: 100%;
  height: 100%;
  display: flex;
  padding: 24px 128.56px 24px;
  background: #f7f7f7;
}
.asside {
  width: 223px;
  height: 100%;
  background: #fff;
  border-radius: 6px;
  overflow: hidden;
}
.menu {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 88vh;
  font-family: \601d\6e90\9ed1\4f53;
}
.top {
  display: flex;
  position: relative;
  align-items: center;
  left: 50%;
  transform: translate(-50%);
  margin-top: 50px;
  width: 149px;
  height: 56px;
}
.head {
  position: relative;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  overflow: hidden;
  background: gray;
}
.menu .top .head img {
  position: absolute;
  top: 10px;
  width: 56px;
  height: 56px;
}
.menu .top .name {
  flex: 1;
  max-width: 60px;
  height: 30px;
  line-height: 30px;
  position: relative;
  margin-left: 29px;
}
.el-menu {
  flex: 1;
  margin-top: 50px;
  background: #fff;
  border: none;
}
.el-menu-item {
  display: flex;
  align-items: center;
  height: 56px;
  line-height: 56px;
  font-size: 14px;
  color: rgb(48, 49, 51);
  list-style: none;
  cursor: pointer;
  position: relative;
  box-sizing: border-box;
  white-space: nowrap;
}
.el-menu-item.is-active {
  color: #409eff;
}

.right {
  width: 100%;
  flex: 1;
  margin-left: 30px;
  height: 100%;
  background: #fff;
  border-radius: 6px;
}

.menu {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 88vh;
}
.works {
  display: flex;
  flex-direction: column;
  width: 1033px;
  height: 100%;
  padding: 32px;
  background: #fff;
}
.title {
  font-size: 18px;
  font-weight: 500;
  letter-spacing: 0px;
  line-height: 26px;
  font-family: \601d\6e90\9ed1\4f53;
}
.el-button {
  margin-top: 24px;
  color: #ffffff;
  height: 32px;
  font-weight: 500;
  background-color: rgb(27, 99, 171);
  padding: 8px 15px;
  font-size: 14px;
  border-radius: 4px;
  text-align: left;
}
.right.left {
  text-align: left;
}
.works .table {
  margin-top: 24px;
}
</style>