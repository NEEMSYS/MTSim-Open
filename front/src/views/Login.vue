<template>
  <div class="login-container">
    <el-row>
      <el-col :span="10">
        <el-tabs class="tab-pages">
          <el-tab-pane label="登录">
            <el-form
              ref="loginForm"
              label-position="left"
              autocomplete="on"
              :model="loginForm"
              :rules="Loginrules"
            >
              <div class="title-container">
                <h3 class="title">登录</h3>
                <el-form-item>
                  <span class="svg-container">
                    <i class="el-icon-user"></i>
                  </span>
                  <el-input
                    prop="username"
                    tabindex="1"
                    placeholder="Username"
                    v-model="loginForm.username"
                    autocomplete="on"
                  ></el-input>
                </el-form-item>
                <el-form-item>
                  <span class="svg-container">
                    <i class="el-icon-lock"></i>
                  </span>
                  <el-input
                    prop="password"
                    tabindex="2"
                    placeholder="Password"
                    type="password"
                    v-model="loginForm.password"
                    autocomplete="off"
                  ></el-input>
                </el-form-item>
                <el-button
                  class="btn"
                  style="width: 100%; margin-top: 40px; margin-bottom: 50px"
                  @click.native.prevent="handLogin('loginForm')"
                  >登录</el-button
                >
              </div>
            </el-form>
          </el-tab-pane>
          <el-tab-pane label="注册">
            <el-form
              ref="registerForm"
              label-position="left"
              autocomplete="on"
              :model="registerForm"
              :rules="Registerrules"
            >
              <div class="title-container">
                <h3 class="title">注册</h3>
                <el-form-item>
                  <span class="svg-container">
                    <i class="el-icon-user"></i>
                  </span>
                  <el-input
                    prop="username"
                    tabindex="1"
                    placeholder="Username"
                    v-model="registerForm.username"
                    autocomplete="on"
                  ></el-input>
                </el-form-item>
                <el-form-item>
                  <span class="svg-container">
                    <i class="el-icon-lock"></i>
                  </span>
                  <el-input
                    prop="password"
                    tabindex="2"
                    placeholder="Password"
                    type="password"
                    v-model="registerForm.password"
                    autocomplete="off"
                  ></el-input>
                </el-form-item>
                <el-form-item prop="checkpwd">
                  <span class="svg-container">
                    <i class="el-icon-lock"></i>
                  </span>
                  <el-input
                    prop="checkpwd"
                    tabindex="3"
                    type="password"
                    placeholder="Confirm Password"
                    v-model="registerForm.checkpwd"
                    autocomplete="off"
                  ></el-input>
                </el-form-item>
                <el-button
                  class="btn"
                  style="width: 100%; margin-top: 40px; margin-bottom: 50px"
                  @click.native.prevent="handRegister('registerForm')"
                  >注册</el-button
                >
              </div>
            </el-form>
          </el-tab-pane>
        </el-tabs>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  data() {
    var validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        if (this.registerForm.checkpwd !== "") {
          this.$refs.registerForm.validateField("checkpwd");
        }
        callback();
      }
    };
    var validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.registerForm.password) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    return {
      registerForm: {
        username: null,
        password: null,
        checkpwd: null,
      },
      loginForm: {
        username: null,
        password: null,
      },
      Loginrules: {
        username: [
          {
            required: true,
            message: "请输入用户名",
            trigger: "blur",
          },
        ],
        password: [
          {
            required: true,
            message: "请输入密码",
            trigger: "blur",
          },
        ],
      },
      Registerrules: {
        username: [
          {
            required: true,
            message: "请输入用户名",
            trigger: "blur",
          },
          {
            min: 6,
            max: 15,
            message: "长度在 6 到 15 个字符",
            trigger: "blur",
          },
        ],
        password: [
          {
            required: true,
            message: "请输入密码",
            trigger: "blur",
          },
          {
            min: 6,
            max: 10,
            message: "长度在 6 到 15 个字符",
            trigger: "blur",
          },
          {
            validator: validatePass,
            trigger: "blur",
          },
        ],
        checkpwd: [
          {
            required: true,
            message: "请再次输入密码",
            trigger: "blur",
          },
          {
            min: 6,
            max: 15,
            message: "长度在 6 到 10 个字符",
            trigger: "blur",
          },
          {
            validator: validatePass2,
            trigger: "blur",
          },
        ],
      },
    };
  },
  components: {},
  methods: {
    handLogin(formName) {
      // 清除上一次登录过的缓存
      localStorage.clear();
      sessionStorage.clear();
      const msg = this;
      this.$refs[formName].validate((valide) => {
        if (valide) {
          axios
            .post(`api/jwt-auth/`, this.loginForm)
            .then((res) => {
              // console.log(res.data); //处理成功的函数 相当于success
              if (res.status == 200) {
                this.$message({
                  message: "登录成功",
                  type: "success",
                });
                // 更新缓存
                this.$store.commit("setUser", res.data.user);
                this.$store.commit("setUserinfo", res.data.userinfo);
                this.$store.commit("setAuthorization", res.data.token);
                if (res.data && res.data.attend) {
                  // 如果res.data存在且res.data.attend不为空，则执行commit
                  this.$store.commit("setAttend", res.data.attend);
                }
                this.$store.commit("setIsLoggedIn", true);
                this.$router.push("/");
              }
            })
            .catch(function (error) {
              //错误处理 相当于error
              msg.$message("登录失败，账号或密码错误");
              console.log(error);
            });
        } else {
          //表单验证失败
        }
      });
    },
    handRegister(formName) {
      const msg = this;
      this.$refs[formName].validate((valide) => {
        if (valide) {
          axios
            .post(`api/register/`, this.registerForm)
            .then((res) => {
              console.log(res); //处理成功的函数 相当于success
              if (res.status == 200) {
                this.$message({
                  message: "注册成功",
                  type: "success",
                });
              } else {
                this.$message({
                  message: res.data.msg,
                  type: "error",
                });
              }
            })
            .catch(function (error) {
              msg.$message("注册失败");
              console.log(error); //错误处理 相当于error
            });
        } else {
          //表单验证失败
        }
      });
    },
  },
};
</script>

<style lang="scss" scoped>
@import "../assets/css/app.8dfc3557.css";
// #login-from {
//   margin: 50px 540px;
//   width: 400px;
//   height: 400px;
//   border-radius: 10px;
//   background-color: #ffffff;
// }

.btn {
  color: rgb(255, 255, 255);
  text-align: center;
  background: rgb(12, 64, 145);
  border-radius: 17px;
}

.text-foot {
  // text-align: center;
  // padding: 10px;
  font-weight: 700;
  margin-top: 20px;
  // color: var(--color-semidark);
}
.el-tabs__item {
  font-size: 16px;
}
</style>
