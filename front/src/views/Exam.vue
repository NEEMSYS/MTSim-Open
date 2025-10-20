<template>
  <div id="exam">
    <div style="width: 100%; height: 100%">
      <el-row style="margin-left: -10px; margin-right: -10px">
        <el-col
          :span="18"
          :offset="3"
          style="padding-left: 10px; padding-right: 10px"
        >
          <div class="title">
            <h1>场景可视化下载</h1>
          </div>
          <div class="chooser">
            <el-form
              :inline="true"
              :model="formInlines"
              class="demo-form-inline"
            >
              <el-form-item label="路网类型">
                <el-select v-model="formInlines.types">
                  <el-option label="直线路段" value="直线路段"></el-option>
                  <el-option label="车辆汇入" value="车辆汇入"></el-option>
                  <el-option label="车辆汇出" value="车辆汇出"></el-option>
                </el-select>
              </el-form-item>

              <el-form-item label="车道数量">
                <el-select v-model="formInlines.lines">
                  <el-option lable="2" value="2"></el-option>
                  <el-option lable="3" value="3"></el-option>
                  <el-option lable="4" value="4"></el-option>
                </el-select>
              </el-form-item>

              <el-form-item label="每小时通过车辆的数量">
                <el-select v-model="formInlines.vehsPerHour">
                  <el-option label="1500" value="1500"></el-option>
                  <el-option label="2000" value="2000"></el-option>
                  <el-option lbael="2500" value="2500"></el-option>
                </el-select>
              </el-form-item>

              <el-form-item label="渗透率">
                <el-select v-model="formInlines.permeability">
                  <el-option label="0" value="0"></el-option>
                  <el-option label="10%" value="10%"></el-option>
                  <el-option label="20%" value="20%"></el-option>
                  <el-option label="30%" value="30%"></el-option>
                  <el-option label="40%" value="40%"></el-option>
                  <el-option label="50%" value="50%"></el-option>
                  <el-option label="60%" value="60%"></el-option>
                  <el-option label="70%" value="70%"></el-option>
                  <el-option label="80%" value="70%"></el-option>
                  <el-option label="90%" value="80%"></el-option>
                  <el-option label="100%" value="100"></el-option>
                </el-select>
              </el-form-item>

              <div class="submit">
                <el-form-item>
                  <el-button type="primary" @click="choose(formInlines)"
                    >筛选</el-button
                  >
                  <el-button @click="reset(formInlines)">重置</el-button>
                </el-form-item>
              </div>
            </el-form>
          </div>
          <div style="margin-top: 20px">
            <el-table
              :data="pagination.results"
              stripe
              style="width: 100%"
              size="medium"
            >
              <el-table-column type="expand">
                <template>
                  <el-col
                    :span="12"
                    style="padding-left: 10px; padding-right: 10px"
                  >
                    <h2>详情:</h2>
                    <div class="block">
                      <el-image
                        style="width: 100%; height: 100%"
                        :src="require('@/assets/SD.gif')"
                      ></el-image>
                    </div>
                  </el-col>
                </template>
              </el-table-column>
              <el-table-column prop="name" label="场景文件名称">
              </el-table-column>
              <el-table-column prop="types" label="路网类型"> </el-table-column>
              <el-table-column prop="lines" label="车道数量"> </el-table-column>
              <el-table-column prop="vehsPerHour" label="每小时车辆通过数量">
              </el-table-column>
              <el-table-column prop="permeability" label="渗透率">
              </el-table-column>

              <el-table-column prop="file" label="下载链接" width="200">
                <template slot-scope="scope">
                  <el-button type="primary" @click="download(scope.row.file)"
                    >场景下载</el-button>
                </template>
              </el-table-column>

              <el-table-column prop="docfile" label="场景文档下载" width="200">
                <template slot-scope="scope">
                  <el-button type="primary" @click="download(scope.row.docfile)"
                    >文档下载</el-button>
                </template>
              </el-table-column>

            </el-table>
            <Pagination
              :count="pagination.count"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            ></Pagination>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination.vue";
export default {
  data() {
    return {
      // 初始化下载数据为空
      formInlines: {
        types: null,
        lines: null,
        vehsPerHour: null,
        permeability: null,
      },
      loading: false,
      page: 1,
      page_size: 10,
      pagination: {
        count: null,
        next: null,
        previous: null,
        results: [],
      },
    };
  },
  components: {
    Pagination,
  },
  mounted() {
    this.getFileInfo(); //在mounted钩子函数中调用加载数据的方法
  },
  methods: {
    //下载信息
    download(fileUrl) {
      window.location.href = fileUrl;
    },
    // 发送请求
    getFileInfo() {
      axios
        .get("api/scenarios/", {
          params: {
            page: this.page,
            page_size: this.page_size,
          },
        }) //发起get请求并指定后端
        .then((response) => {
          console.log(response.data);
          this.pagination = response.data;
        })
        .catch((error) => {
          console.log("Error:", error);
        });
    },

    choose(formName) {
      axios
        .get("api/filterScenarios/", {
          params: {
            formInlines: this.formInlines,
            page: this.page,
            page_size: this.page_size,
          },
        })
        .then((response) => {
          console.log(response.data);
          this.pagination = response.data;
        });
    },
    //改变每页条数
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
      this.page_size = val;
      this.getFileInfo();
    },
    //跳转到多少页
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.page = val;
      this.getFileInfo();
    },
  },
};
</script>

<style>
@import "../assets/css/app.8dfc3557.css";
.title {
  margin-top: 20px;
}
.submit {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}

.cell {
  text-align: center;
  color: #303133;
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
.block {
  text-align: left;
  display: flex;
  justify-content: right;
}
.el-image {
  position: relative;
  display: inline-block;
  overflow: hidden;
}
</style>
