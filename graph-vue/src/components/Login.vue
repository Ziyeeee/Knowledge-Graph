<template>
  <div>
    <div class="background">
      <img src="../loginbg.jpg" class="image"/>
    </div>
    <div class="loginbody">
      <div>
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
  </div>
</template>
<script>
export default {
  name: "Login",
  // imgSrc:require('./src/loginbg.jpg'),
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
  // created () {
  //   if(JSON.parse( localStorage.getItem('user')) && JSON.parse( localStorage.getItem('user')).username){
  //     this.username = JSON.parse( localStorage.getItem('user')).username;
  //     this.password = JSON.parse( localStorage.getItem('user')).password;
  //   }
  // },
  methods: {
    doLogin() {
      // eslint-disable-next-line no-unused-vars
      const {username, password, $router} = this
      if (username === "zhounan" && password === "zhou20010429") {
        this.$router.push({
          name:'main',
          params:{
            username:this.username
          }
        })
      } else {
        alert('用户名错误')
      }
    }
  }
}
</script>
<style>
  .loginbody{
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100%;
    height: 100%;
    /*display: flex;*/
    /*justify-content: center;*/
    /*align-items: center;*/
    z-index: 1;
    margin: -200px 0 0 -200px;
  }
  .background{
    width:100%;
    height:100%;  /**宽高100%是为了图片铺满屏幕 */
    z-index:-1;
    position: absolute;
  }
  .image{
    height: 100%;
    width: 100%;
    opacity: 80%;
  }
</style>