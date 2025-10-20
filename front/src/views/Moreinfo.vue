<template>
  <div id="moreinfo">
    <el-container>
      <el-header>
        <h1 style="color: #ffffff; margin-top: 50px">{{ getUser.username }}</h1>
      </el-header>
      <el-main>
        <div id="moreinfo-from">
          <el-form
            ref="registerForm"
            status-icon
            :model="registerForm"
            :rules="rules"
          >
            <el-form-item label="用户名" prop="name">
              <el-input
                v-model="registerForm.username"
                autocomplete="off"
              ></el-input>
            </el-form-item>
            <el-form-item label="姓名" prop="name">
              <el-input
                v-model="registerForm.name"
                autocomplete="off"
              ></el-input>
            </el-form-item>
            <el-form-item label="年龄" prop="age">
              <el-input
                v-model="registerForm.age"
                autocomplete="off"
              ></el-input>
            </el-form-item>
            <el-form-item label="性别" prop="gender">
              <el-select v-model="registerForm.gender" placeholder="请选择性别">
                <el-option label="男" value="m"></el-option>
                <el-option label="女" value="g"></el-option>
              </el-select>
            </el-form-item>
            <br />
            <el-button type="primary">注册</el-button>
          </el-form>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      input: this.Username,
      registerForm: {
        name: null,
        age: null,
        gender: null,
        user: null,
        username: null,
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
        age: [
          {
            required: true,
            message: "请输入年龄",
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
      },
    };
  },
  methods: {
    created() {
      this.registerForm = this.$store.state.user;
    },
    Username() {
      return getUser.username;
    },
  },
  computed: {
    getUser() {
      return this.$store.state.user;
    },
  },
};
</script>

<style lang="scss" scoped>
#moreinfo {
  // height: 700px;
  /* background-color: #244d6f; */
  background-image: url(../assets/bg.jpg);
  background-repeat: no-repeat;
  background-size: cover;
}

#moreinfo-from {
  margin: 0px 540px;
  width: 400px;
  height: 600px;
  border-radius: 10px;
  background-color: #ffffff;
}

.el-form {
  padding-top: 20px;
  margin: 50px 50px;
  width: 300px;
}

// .el-input {
// }

.el-button {
  width: 100%;
}

.text-foot {
  font-weight: 700;
  margin-top: 20px;
}
</style>
  