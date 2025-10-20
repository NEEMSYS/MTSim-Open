<template>
  <div id="competition">
    <el-card shadow="always" style="min-height: 700px">
      <div class="card-content" style="margin: 40px">
        <h1 style="text-align: left">所有比赛</h1>
        <div>
          <el-table :data="tableData" style="width: 100%">
            <el-table-column prop="name" label="比赛" width="480">
            </el-table-column>
            <el-table-column label="提交类型" width="200">
              <template> Docker ID </template>
            </el-table-column>
            <el-table-column prop="number" label="参与人数" width="200">
            </el-table-column>
            <el-table-column label="参与情况" width="100">
              <template slot-scope="scope">
                <div class="redBk" v-if="islogin && isRegistered(scope.row.id)">
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
          </el-table>
        </div>
      </div>
    </el-card>
    <!-- && isRegistered(scope.row.id) -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      // 初始化数据为空
      islogin: false,
      tableData: null,
    };
  },
  created() {
    this.islogin = this.$store.state.isLoggedIn;
  },
  computed: {
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
  mounted() {
    this.getCompetitionInfo();
  },
  methods: {
    //获取所有的比赛信息
    getCompetitionInfo() {
      axios
        .get("api/competition/") //发起get请求并指定后端
        .then((response) => {
          // 此处的response.data是个数据, 经过后端序列化后的数据
          this.tableData = response.data;
        })
        .catch((error) => {
          console.log("Error:", error);
        });
    },
    //报名
    application(id) {
      if (!this.islogin) {
        this.$router.push({
          name: "Login",
        });
      } else {
        const userId = this.$store.state.user.id; // 提取用户ID到变量中，便于阅读
        const competitionId = id; // 提取比赛ID到变量中
        console.log({
          user: userId,
          competition: competitionId,
        });
        axios
          .post(`api/participant/`, {
            user: userId,
            competition: competitionId,
          })
          .then((res) => {
            console.log(res); //处理成功的函数 相当于success
            if (res.status == 201) {
              this.$message({
                message: "报名成功",
                type: "success",
              });
              // 更新缓存
              this.$store.commit("setAttend", [
                {
                  user: userId,
                  competition: competitionId,
                },
              ]);
            }
          });
      }
    },
    // 此处的id是比赛的id,发送get请求看是否能返回数据
    // 检查用户是否报名该比赛
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
#competition {
  margin: 0px 150px;
}

h1 {
  margin-top: 40px;
  color: #14579e;
  font-weight: 700;
  font-size: 35px;
  // margin: 0.67em 0;
}

.el-table {
  font-size: 18px;
}
.redBk {
  text-align: center;
  font-size: 12px;
  border-radius: 6px;
  padding: 5px;
  box-sizing: border-box;
  color: #f56c6c;
  border: 1.5px solid #f56c6c;
}
</style>