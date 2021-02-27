<template>
  <div class="center">
    <div id="login">
      <el-card style="width: 400px">
        <div slot="header" class="clearfix">
          <span>登录</span>
        </div>
        <table>
          <tr>
            <td>用户名</td>
            <td>
              <el-input v-model="username" placeholder="请输入用户名"></el-input>
            </td>
          </tr>
          <tr>
            <td>密码</td>
            <td>
              <el-input type="password" v-model="password" placeholder="请输入密码" @keydown.enter.native="doLogin"></el-input>
              <!-- @keydown.enter.native="按下enter键的时候也会执行doLogin-->
            </td>
          </tr>
          <tr>
            <td colspan="2">
              <el-button style="width: 300px" type="primary" @click="doLogin">登录</el-button>
            </td>
          </tr>
        </table>
      </el-card>
    </div>
  </div>
</template>
<script>
export default {
  name: "Login",
  props: {
    msg: String
  },
  data() {
    return {
      username: '',
      password: '',
      error: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    check(username, password) {
      if (!username) {
        this.error.username = '请输入姓名'
        return false
      }
      if (!username) {
        this.error.password = '请输入密码'
        return false
      }
    },
    doLogin() {
      // const {username, password, $router} = this
      // if (!this.check(username, password)) return
      //
      // if (username == 'zhounan' && password == 'zhou20010429') {
      //   $.router.push({name: 'main'})
      // } else {
      //   alert('用户名错误')
      // }
    }
  }
}
</script>
<style>
  /*#login{*/
  /*  !*display: flex;*!*/
  /*  !*justify-content: center;*!*/
  /*  !*margin-top: 150px;*!*/
  /*  position: absolute;*/
  /*  top: 50%;*/
  /*  left: 50%;*/
  /*  margin: -200px 0 0 -200px;*/
  /*}*/
  .center{
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
</style>
