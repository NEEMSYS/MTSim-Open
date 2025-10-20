<template>
  <div id="center">
    <h1 style="text-align: left">个人信息</h1>
    <el-card
      shadow="always"
      style="width: 80%; margin-left: 10%; margin-bottom: 80px"
    >
      <div class="card-content">
        <el-form
          ref="centerForm"
          status-icon
          :model="centerForm"
          :rules="rules"
          label-width="85px"
        >
          <el-form-item label="姓名" prop="name">
            <el-input v-model="centerForm.name"></el-input>
          </el-form-item>
          <el-form-item label="年龄" prop="age">
            <el-input v-model="centerForm.age"></el-input>
          </el-form-item>
          <el-form-item label="性别" prop="gender">
            <el-select v-model="centerForm.gender" placeholder="请选择性别">
              <el-option label="男" value="m"></el-option>
              <el-option label="女" value="g"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="centerForm.email"></el-input>
          </el-form-item>
          <el-form-item>
            <!-- 此处点击按钮发送请求，进行修改 -->
            <el-button type="primary" @click="updateInfo('centerForm')"
              >确认修改</el-button
            >
            <el-button @click="cancel">取消</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      centerForm: {
        name: null,
        gender: null,
        age: null,
        user: null,
        email: null,
      },
      rules: {
        name: [
          {
            required: true,
            message: "请输入姓名",
            trigger: "blur",
          },
          {
            min: 2,
            max: 10,
            message: "长度在 2 到 8 个字符",
            trigger: "blur",
          },
        ],
        gender: [
          {
            required: true,
            message: "请选择性别",
            trigger: "change",
          },
        ],
        age: [
          {
            required: true,
            message: "请输入年龄",
            trigger: "blur",
          },
        ],
        email: [
          {
            required: true,
            message: "请输入邮箱",
            trigger: "blur",
          },
        ],
      },
    };
  },
  methods: {
    updateInfo(formName) {
      this.$refs[formName].validate((valide) => {
        console.log(this.centerForm);
        if (valide) {
          console.log(this.centerForm);
          this.$axios
            .patch(
              `/api/userinfo/${this.centerForm.id}/?format=json`,
              this.centerForm
            )
            .then((res) => {
              console.log(res);
              if (res.status == 200) {
                this.$message({
                  message: "更新个人信息成功",
                  type: "success",
                });
                //更新缓存
                this.$store.commit("setUserinfo", this.centerForm);
              } else {
                this.$message({
                  message: "更新个人信息失败",
                  type: "error",
                });
              }
            })
            .catch((error) => {
              console.log(error);
            });
        } else {
          //表单验证失败
        }
      });
    },
    cancel() {
      this.$router.push("/");
    },
  },
  created() {
    this.centerForm = this.$store.state.userinfo;
  },
};
</script>

<style lang="scss" scoped>
h1 {
  margin-left: 10%;
  margin-top: 40px;
  color: #14579e;
  font-weight: 700;
  font-size: 35px;
  // margin: 0.67em 0;
}

.el-form {
  width: 400px;
}

.el-select {
  width: 320px;
}

// .el-input {
// }
</style>
