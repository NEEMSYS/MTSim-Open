<template>
  <div id="layout">
    <div class="container">
      <el-header class="header-layout">
        <el-row style="margin-left: -10px; margin-right: -10px">
          <el-col :span="22" style="padding-left: 100px; padding-right: 10px">
            <div class="nav-menu">
              <el-menu
                mode="horizontal"
                style="line-height: 60px; background: rgb(20, 87, 158)"
                active-text-color="#fff"
                :router="true"
              >
                <el-menu-item class="hang" index="/">首页</el-menu-item>
                <el-menu-item class="hang" index="/exam">场景</el-menu-item>
                <el-submenu index="2">
                  <template slot="title"
                    ><span style="color: #fff">比赛</span></template
                  >
                  <el-menu-item
                    class="lie"
                    index="/grade"
                    style="color: #000000a6"
                    >排行榜</el-menu-item
                  >
                  <el-menu-item
                    class="lie"
                    index="/competition"
                    style="color: #000000a6"
                    >所有比赛</el-menu-item
                  >
                </el-submenu>
              </el-menu>
            </div>
          </el-col>
          <el-col :span="2" style="padding-left: 10px; padding-right: 10px">
            <el-button class="loginBtn" v-if="!isLoggedIn" @click="toLogin">
              <span>登录</span>
            </el-button>
          </el-col>
          <el-col :span="2" style="padding-left: 10px; padding-right: 10px">
            <el-dropdown class="dropdown" v-if="isLoggedIn">
              <span class="el-dropdown-link">
                {{ getUser.username }}
                <i class="el-icon-caret-bottom"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <a href="center">
                  <el-dropdown-item> 个人中心 </el-dropdown-item></a
                >
                <a href="password">
                  <el-dropdown-item>修改密码</el-dropdown-item></a
                >
                <a href="mygame">
                  <el-dropdown-item>我的比赛</el-dropdown-item></a
                >
                <a href="MyCustomWorks">
                  <el-dropdown-item>自定义场景</el-dropdown-item></a
                >
                <el-dropdown-item divided>
                  <el-button @click="loginOut">退出登录</el-button>
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </el-col>
        </el-row>
      </el-header>
    </div>
    <section class="app-main">
      <router-view />
    </section>

    <!-- <el-footer>
        <b>@Copyright 2019-2020. ALL Rights Reserved</b>
      </el-footer> -->
  </div>
</template>

<script>
export default {
  name: "layout",
  data() {
    return {};
  },
  computed: {
    isLoggedIn() {
      return this.$store.state.isLoggedIn;
    },
    getUser() {
      return this.$store.state.user;
    },
  },
  methods: {
    toLogin() {
      this.$router.push({
        name: "Login",
        params: {},
      });
    },
    loginOut() {
      this.$router.push("/");
      this.$store.commit("setIsLoggedIn", false);
      sessionStorage.clear();
      localStorage.clear();
    },
  },
  created() {},
};
</script>

<style lang="scss" scoped>
@import "../assets/css/app.8dfc3557.css";

.container {
  height: 60px;
  overflow: hidden;
  position: relative;
  background: #000;
}

// 设置header的属性，line-height为行高
.header-layout {
  height: 65px !important;
  padding: 0 50px;
  line-height: 64px;
  background: #14579e;
}
// 取消链接的下划线
a {
  text-decoration: none;
}

// 放置菜单栏的盒子
.nav-menu {
  width: 100%;
  height: 100%;
}
.hang {
  color: #fff !important;
  background: rgb(20, 87, 158) !important;
  font-size: 14px;
}
.hang:hover 
  /* 当鼠标悬停时，设置您想要的背景色 */ {
  background-color: #0c4091 !important; /* 替换为您想要的背景色 */
}

.dropdown {
  float: right;
  margin-bottom: auto;
  margin-left: auto;
  height: 100%;
  line-height: 50px;
}

.el-dropdown-link {
  color: #fff;
  font-size: 14px;
}
.app-main {
  min-height: calc(100vh - 50px);
  width: 100%;
  position: relative;
  overflow: hidden;
}
.loginBtn {
  background: #14579e;
  color: #fff;
}
</style>
