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
              <div class="title">作品管理</div>
              <div class="left">
                <el-button :disabled="shouldisDisabled" @click="Upload = true">
                  <i class="el-icon-upload2"> 作品上传</i>
                </el-button>
                <!-- 对话框 -->
                <el-dialog
                  :visible.sync="Upload"
                  @close="Upload = false"
                  width="400px"
                  title="上传信息"
                >
                  <el-form :model="WorksData" ref="WorksData">
                    <el-form-item
                      label="Docker ID"
                      prop="dockerId"
                      :rules="[
                        {
                          required: true,
                          message: '请输入Docker ID',
                          trigger: 'blur',
                        },
                      ]"
                      :label-width="formLabelWidth"
                    >
                      <el-input
                        style="width: 240px"
                        v-model="WorksData.dockerId"
                      ></el-input>
                    </el-form-item>
                    <el-form-item
                      label="比赛名称"
                      prop="competition_name"
                      :label-width="formLabelWidth"
                      :rules="[
                        {
                          required: true,
                          message: '请选择比赛名称',
                          trigger: 'change',
                        },
                      ]"
                    >
                      <el-select
                        v-model="WorksData.competition_name"
                        placeholder="请选择"
                      >
                        <el-option
                          label="第一届混合交通流控制算法竞赛"
                          value="第一届混合交通流控制算法竞赛"
                        ></el-option>
                        <el-option
                          label="第二届混合交通流控制算法竞赛"
                          value="第二届混合交通流控制算法竞赛"
                        ></el-option>
                        <el-option
                          label="第三届混合交通流控制算法竞赛"
                          value="第三届混合交通流控制算法竞赛"
                        ></el-option>
                      </el-select>
                    </el-form-item>
                  </el-form>

                  <div slot="footer" class="dig-footer">
                    <!-- SubmitData('WorksData')RunDcoker() -->
                    <el-button type="primary" @click="RunDocker()"
                      >确定</el-button
                    >
                    <el-button @click="Upload = false">取消</el-button>
                  </div>
                </el-dialog>

              <!-- 新增场景生成按钮 -->
              <el-button @click="showScenarioDialog = true">
                <i class="el-icon-setting"> 生成场景</i>
              </el-button>
                    <!-- 新增场景生成对话框 -->
                        <el-dialog
                              :visible.sync="showScenarioDialog"
                              title="生成测试场景"
                              width="500px"
                          >
                              <el-form :model="scenarioForm" label-width="100px">
                                  <el-form-item label="场景类型">
                                      <el-select 
                                          v-model="scenarioForm.type" 
                                          placeholder="请选择"
                                      >
                                          <el-option 
                                              label="直线路段" 
                                              value="straight"
                                          ></el-option>
                                          <el-option 
                                              label="交叉路口" 
                                              value="intersection"
                                          ></el-option>
                                      </el-select>
                                  </el-form-item>
                                  <el-form-item label="车道数量">
                                      <el-input-number 
                                          v-model="scenarioForm.lanes" 
                                          :min="1" 
                                          :max="6"
                                      ></el-input-number>
                                  </el-form-item>
                                  <el-form-item label="渗透率(%)">
                                      <el-input-number          
                                          v-model="scenarioForm.penetration" 
                                          :min="0" 
                                          :max="100"
                                      ></el-input-number>
                                  </el-form-item>
                                  <el-form-item label="车辆密度">
                                      <el-slider 
                                          v-model="scenarioForm.density" 
                                          :min="50" 
                                          :max="2000"
                                      ></el-slider>
                                  </el-form-item>
                              </el-form>
                              <div slot="footer">
                                  <el-button @click="showScenarioDialog = false">取消</el-button>
                                  <el-button 
                                      type="primary" 
                                      @click="generateScenario"
                                  >生成</el-button>
                              </div>
                          </el-dialog>
                          
                     <!-- <el-button 
                @click="downloadScenario=true">
                下载自定义场景
            </el-button> -->
              <el-button @click="showCustomTestDialog = true">
          <i class="el-icon-setting"> 测试自定义场景</i>
          </el-button>

<el-dialog :visible.sync="showCustomTestDialog" @close="showCustomTestDialog = false" title="测试自定义场景">
  <el-form :model="customTestForm" ref="customTestForm" :rules="customTestRules">
    <el-form-item 
      label="场景类型" 
      prop="scenario_type"
      :rules="[{ required: true, message: '请选择场景类型', trigger: 'change' }]">
      <el-select 
        v-model="customTestForm.scenario_type" 
        placeholder="请选择"
      >
        <el-option 
          label="直线路段" 
          value="straight"
        ></el-option>
        <el-option 
          label="交叉路口" 
          value="intersection"
        ></el-option>
      </el-select>
    </el-form-item>
    
    <el-form-item 
      label="比赛名称" 
      prop="competition_name"
      :rules="[{ required: true, message: '请输入比赛名称', trigger: 'blur' }]">
      <el-input v-model="customTestForm.competition_name"></el-input>
    </el-form-item>
    
    <el-form-item 
      label="Docker ID" 
      prop="dockerId"
      :rules="[{ required: true, message: '请输入Docker ID', trigger: 'blur' }]">
      <el-input v-model="customTestForm.dockerId"></el-input>
    </el-form-item>
  </el-form>
  
  <div slot="footer">
    <el-button @click="showCustomTestDialog = false">取消</el-button>
    <el-button 
      type="primary" 
      @click="testCustomScenario"
    >开始测试</el-button>
  </div>
</el-dialog>

                <el-button @click="pushgrade">排行榜信息</el-button>
              </div>
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
                    width="220px"
                  >
                  </el-table-column>
                  
                  <el-table-column
                    prop="scenario_des"
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
      Upload: false,
      gameData: [],
      scenarioForm: {
      type: 'straight',  // default scenario type
      lanes: 2,         // default number of lanes
      penetration: 50,  // default penetration rate
      density: 200 ,     // default vehicle density
      result_file: ''
    },
      // 新增场景相关数据
  showCustomTestDialog: false,
    customTestForm: {
      scenario_type: null,
      competition_name: null,
      dockerId: null,
      add_time: null,
      username: null
    },
    showScenarioDialog:false,
      // 提交作品的基础信息
      formLabelWidth: "100px",
      WorksData: {
        username: null,
        competition_name: null,
        dockerId: null,
        add_time: null,
      },
      customTestRules: {
        scenario_type: [
          { required: true, message: '请选择场景类型', trigger: 'change' }
        ],
        competition_name: [
          { required: true, message: '请输入比赛名称', trigger: 'blur' }
        ],
        dockerId: [
          { required: true, message: '请输入Docker ID', trigger: 'blur' }
        ]
      },
    };
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
    shouldisDisabled() {
      return this.competitions.length === 0;
    },
    getUser() {
      return this.$store.state.user;
    },
  },
  created() {
    this.WorksData.username = this.$store.state.user.username;
    this.customTestForm.username = this.$store.state.user.username;
    this.islogin = this.$store.state.isLoggedIn;
    this.MySubmit();
  },
  mounted() {},

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
    getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // 找到名为csrftoken的cookie
          if (cookie.substring(0, 10) === "csrftoken=") {
            cookieValue = decodeURIComponent(cookie.substring(10));
            break;
          }
        }
      }
      return cookieValue;
    },

    handleScenarioTypeChange(value) {
  if (value) {
    this.$refs.customTestForm.validate(valid => {
      if (valid) {
        this.userSubmitData('customTestForm');
      }
    });
  }
},
// 修改后的 SubmitData 方法，返回 Promise
SubmitData(formName) {
  return new Promise((resolve, reject) => {
    this.$refs[formName].validate((valid) => {
      if (valid) {
        axios.post("api/submitWorks/", this.WorksData)
          .then((res) => {
            if (res.status === 201) {
              this.$message({
                message: "提交成功",
                type: "success",
              });
              this.Upload = false;
              resolve(res); // 成功时 resolve
            } else {
              this.$message({
                message: "提交失败",
                type: "error",
              });
              reject(new Error("提交失败")); // 失败时 reject
            }
          })
          .catch((error) => {
            console.log(error.response);
            reject(error); // 捕获错误并 reject
          });
      } else {
        reject(new Error("表单验证失败")); // 验证失败时 reject
      }
    });
  });
},

// 修改后的 RunDocker 方法，使用 async/await 确保顺序
async RunDocker() {
  try {
    const currentTime = new Date();
    const chinaDate = new Date(currentTime.getTime() + 8 * 60 * 60 * 1000);
    const chinaTimeISO = chinaDate.toISOString().slice(0, 19).replace("T", " ");
    this.WorksData.add_time = chinaTimeISO;

    // 先等待 SubmitData 完成
    await this.SubmitData("WorksData");
  
    // SubmitData 成功后再执行后续请求
    axios.post(
      "/api/run/",
      {
        dockerId: this.WorksData.dockerId,
        username: this.WorksData.username,
        add_time: this.WorksData.add_time,
        competition_name: this.WorksData.competition_name,
      },
      {
        headers: {
          "X-CSRFToken": this.getCookie("csrftoken"),
        },
      }
    )
      .then((response) => {
        if (response.status === 200) {
          console.log("Docker 运行成功", this.WorksData, this.result_file = response.data.result_file);
          // 将完整URL保存到gameData
          this.gameData.push({
                ...response.data,
                result_file: response.data.result_file
      });
        }else {
      throw new Error("后端未返回有效文件路径");
    }
      })
      .catch((error) => {
        console.error("Docker 运行失败:", error);
      });
  } catch (error) {
    console.error("保存数据失败:", error);
  }
},

    MySubmit() {
      axios
        .get(`api/myWorks/?username=${this.WorksData.username}`)
        .then((res) => {
          this.gameData = res.data;
        });
    },
    async generateScenario() {
      try {
        const response = await axios.post('/api/generate_scenario/', {
          username: this.WorksData.username,
          ...this.scenarioForm
        }, {
          headers: {
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        });
        
        if (response.status === 201) {
          this.$message.success('场景生成成功');
          this.showScenarioDialog = false;
        }
      } catch (error) {
        this.$message.error('场景生成失败');
        console.error(error);
      }
    },
//测试自定义场景
// 修改后的 userSubmitData 方法，返回 Promise
userSubmitData(formName) {
  return new Promise((resolve, reject) => {
    this.$refs[formName].validate((valid) => {
      if (valid) {
        axios.post("api/usersubmitWorks/", this.customTestForm)
          .then((res) => {
            if (res.status === 201) {
              this.$message({
                message: "提交成功",
                type: "success",
              });
              this.showCustomTestDialog = false;
              resolve(res); // 成功时 resolve
            } else {
              this.$message({
                message: "提交失败",
                type: "error",
              });
              reject(new Error("提交失败")); // 失败时 reject
            }
          })
          .catch((error) => {
            console.log(error.response);
            reject(error); // 捕获错误并 reject
          });
      } else {
        reject(new Error("表单验证失败")); // 验证失败时 reject
      }
    });
  });
},

// 修改后的 RunDocker 方法，使用 async/await 确保顺序
async testCustomScenario() {
  try {
    const currentTime = new Date();
    const chinaDate = new Date(currentTime.getTime() + 8 * 60 * 60 * 1000);
    const chinaTimeISO = chinaDate.toISOString().slice(0, 19).replace("T", " ");
    this.customTestForm.add_time = chinaTimeISO;

    // 先等待 SubmitData 完成
    await this.userSubmitData("customTestForm");
  
    // userSubmitData 成功后再执行后续请求
    axios.post(
      "/api/userrun/",
      {
        dockerId: this.customTestForm.dockerId,
        competition_name: this.customTestForm.competition_name,
        scenario_type:this.customTestForm.scenario_type,
       add_time:this.customTestForm.add_time,
       username:this.customTestForm.username
      },
      {
        headers: {
          "X-CSRFToken": this.getCookie("csrftoken"),
        },
      }
    )
      .then((response) => {
        if (response.status === 200) {
          console.log("Docker 运行成功", this.customTestForm);
          this.Upload = false; // 运行成功后关闭对话框
        }
      })
      .catch((error) => {
        console.error("Docker 运行失败:", error);
      });
  } catch (error) {
    console.error("保存数据失败:", error);
  }
},

    fetchScenarios() {
  axios.get('/api/user_scenarios/', {
    params: {
      username: this.WorksData.username
    }
  }).then(response => {
    this.userScenarios = response.data;
  });
},
// downloadScenario(scenarioId) {
//       const username = this.$store.state.user.username;
//       window.location.href = `/api/download_scenario/?username=${username}&scenario_id=${scenarioId}`;
//   },

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