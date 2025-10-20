<template>
  <div id="grade">
    <div class="content">
      <div class="rankingList">
        <div class="cover">
          <figure><img src="../assets/grade.png" class="bg" /></figure>
          <div class="title">
            <div class="left">
              <div class="title1">竞 赛 排 行 榜</div>
              <div class="title2">排行榜分数为审核后得分</div>
            </div>
            <div class="right"><img src="../assets/background.png" /></div>
          </div>
          <div class="bottom"></div>
        </div>
        <div class="content">
          <div class="rank-card">
            <div class="title">第一届混合交通流控制算法竞赛</div>
            <div class="table-content">
              <el-table :data="rankedResults" style="width: 100%">
                <el-table-column prop="rank" label="排名" align="center">
                </el-table-column>
                <el-table-column prop="username" label="用户名" align="center">
                </el-table-column
                ><el-table-column
                  prop="add_time"
                  label="提交时间"
                  align="center"
                >
                </el-table-column>
                <el-table-column prop="score" label="分数" align="center">
                </el-table-column>
              </el-table>
            </div>
            <Pagination
              :count="pagination.count"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            ></Pagination>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination.vue";
export default {
  data() {
    return {
      loading: false,
      page: 1,
      page_size: 5,
      pagination: {
        count: null,
        next: null,
        previous: null,
        results: [],
      },
      websocket: null,
    };
  },
  components: {
    Pagination,
  },
  computed: {
    rankedResults() {
      return this.pagination.results.map((item, index) => ({
        ...item,
        rank: index + 1,
      }));
    },
  },
  created() {
    this.initWebSocket();
    this.getGradeInfo();
  },
  methods: {
    initWebSocket() {
      this.websocket = new WebSocket("ws://114.215.195.207:8000/ws/grades");

      // onmessage回调函数，用来收到服务端给客户端发送的数据
      this.websocket.onmessage = this.handleWeSocketMessage;
    },
    handleWeSocketMessage(event) {
      const data = JSON.parse(event.data);
      //处理数据，只保留每个用户的最高成绩
      const maxScore = {};
      data.forEach((item) => {
        const username = item.username;
        if (!(username in maxScore) || item.score > maxScore[username].score) {
          maxScore[username] = item;
        }
      });
      // 转化为数组形式，并按成绩排序
      const socreResults = Object.values(maxScore).sort(
        (a, b) => b.score - a.score
      );

      // 更新数据
      this.pagination.results = socreResults;
      this.pagination.count = socreResults.length;
    },

    //获取成绩信息
    getGradeInfo() {
      this.$axios
        .get(`api/grades/?format=json`, {
          params: {
            page: this.page,
            page_size: this.page_size,
          },
        })
        .then((res) => {
          // this.pagination = res.data;
          // console.log(res.data);

          //处理数据，只保留每个用户的最高成绩
          const maxScore = {};
          res.data.results.forEach((item) => {
            const username = item.username;
            if (
              !(username in maxScore) ||
              item.score > maxScore[username].score
            ) {
              maxScore[username] = item;
            }
          });
          // 转化为数组形式，并按成绩排序
          const socreResults = Object.values(maxScore).sort(
            (a, b) => b.score - a.score
          );

          // 更新数据
          this.pagination.results = socreResults;
          this.pagination.count = socreResults.length;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    //改变每页条数
    handleSizeChange(val) {
      // console.log(`每页 ${val} 条`);
      this.page_size = val;
      this.getGradeInfo();
    },
    //跳转到多少页
    handleCurrentChange(val) {
      // console.log(`当前页: ${val}`);
      this.page = val;
      this.getGradeInfo();
    },
  },
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
.content {
  width: 100%;
  height: 100%;
  flex: 1;
}
.rankingList {
  font-family: \601d\6e90\9ed1\4f53;
}
.rankingList .cover {
  position: relative;
}

.rankingList .cover figure {
  overflow: hidden;
}
.rankingList .cover figure img {
  height: 380px;
  width: 100%;
  object-fit: cover;
  vertical-align: middle;
}
.rankingList .cover .title {
  position: absolute;
  bottom: 0;
  padding: 0 10vw;
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.rankingList .cover .title .left {
  color: #fff;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.rankingList .cover .title .left .title1 {
  height: 150px;
  font-size: 68px;
  font-weight: 600;
}

.rankingList .cover .title .left .title2 {
  font-size: 20px;
  height: 100px;
}

.rankingList .cover .title .right {
  height: 100%;
  display: flex;
  align-items: flex-end;
}
.rankingList .cover .title img {
  vertical-align: middle;
  transform: translateY(-38px);
  width: 420px;
}

.rankingList .cover .bottom {
  width: 100%;
  height: 40px;
  border-radius: 40px 40px 0 0;
  background-color: #f7f7f7;
  position: absolute;
  bottom: 0;
  left: 0;
  z-index: 2;
}

.rankingList .content {
  padding: 10px 10vw 40px 10vw;
  background-color: #f7f7f7;
}

.rank-card {
  background-color: #fff;
  box-shadow: 0 2px 10px 4px #4b5b6640;
  padding: 24px 32px;
}

.rank-card .title {
  font-size: 28px;
}

.rank-card .table-content {
  padding: 10px 40px 15px 10px;
}

/* 重置表格样式 */
.el-table th > .cell {
  box-sizing: border-box;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: normal;
  overflow-wrap: break-word;
  line-height: 23px;
  padding: 0 12px;
  text-align: center;
  font-size: 18px;
}

#pagination {
  margin-top: 20px;
  display: flex;
  -webkit-box-pack: center;
  justify-content: center;
}
.el-pagination {
  white-space: nowrap;
  padding: 2px 5px;
  color: #303133;
  font-weight: 700;
}
</style>
