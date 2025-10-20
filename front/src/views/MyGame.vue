<template>
  <div id="mygame">
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
            <div class="myGame">
              <div class="title">我的比赛</div>
              <el-table :data="tableData" style="width: 100%">
                <el-table-column
                  prop="name"
                  label="届数"
                  width="480"
                ></el-table-column>
                <el-table-column label="状态" width="100">
                  <template slot-scope="scope">
                    <div
                      class="redBk"
                      v-if="islogin && isRegistered(scope.row.id)"
                    >
                      已报名
                    </div>
                    <el-button
                      v-else
                      type="primary"
                      @click="application(scope.row.id)"
                      >报名</el-button
                    >
                  </template>
                </el-table-column>
                <el-table-column prop="exam_paper" label="试卷下载" width="480">
                  <template slot-scope="scope">
                    <el-button type="primary"   @click="download(scope.row.exam_paper)"
                    >试卷下载</el-button>
                  </template>
                </el-table-column>
              </el-table>
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
      gameData: null,
      // tableData绑定到表格当中
      tableData: [],
    };
  },
  computed: {
    getUser() {
      return this.$store.state.user;
    },
    // 获取此用户的所有比赛的id
    competitions() {
      const userId = this.$store.state.user.id;
      const attendance = this.$store.state.attendances;
      return Array.from(
        new Set(
          attendance
            .filter((attendance) => attendance.user === userId)
            .map((attendance) => attendance.competition)
        )
      );
    },
  },
  created() {
    this.gameData = this.$store.state.attendances;
    this.islogin = this.$store.state.isLoggedIn;
  },
  mounted() {
    this.getCompetitionInfo();
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
    getCompetitionInfo() {
      // console.log(this.gameData);
      // 根据获取到的比赛id,去比赛表中根据比赛id用过get请求来获取比赛名称
      this.gameData.forEach((item) => {
        if (item.competition) {
          // 使用模板字符串来构造 URL
          const url = `api/competition/${item.competition}/`;
          axios
            .get(url) // 对每个 competition 发起 GET 请求
            .then((response) => {
              // 处理每个请求的响应
              // 假设您想要将每个请求的响应数据放入 this.tableData 数组中
              this.tableData.push(response.data);
            })
            .catch((error) => {
              console.log(
                "Error fetching competition data for:",
                item.competition,
                "Error:",
                error
              );
            });
        } else {
          console.warn(
            "No competition property found for an item in gameData:",
            item
          );
        }
      });
    },

    isRegistered(competitionId) {
      // 使用 this 关键字来访问 computed 属性 competitions
      const competition = this.competitions.find(
        (competition) => competition === competitionId
      );
      return !!competition; // 如果 find 找到了元素，则返回 true；否则返回 false
    },
  },
};
</script>
<style lang="scss" scoped>
.content {
  width: 100%;
  flex: 1;
}

.second {
  width: 100%;
  height: 100%;
  display: flex;
  --safe-distance: 10vw;
  padding: 24px var(--safe-distance);
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
.myGame {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  padding: 32px;
  background: #fff;
}
.myGame .title {
  font-size: 18px;
  font-weight: 500;
  letter-spacing: 0px;
  line-height: 26px;
  font-family: \601d\6e90\9ed1\4f53;
}
</style>