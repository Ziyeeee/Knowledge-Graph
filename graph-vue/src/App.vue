<template>
  <div id="app">
    <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    <!-- <GraphVue></GraphVue>-->
    <el-container direction="vertical">
      <Header msg="面 向 课 程 的 知 识 图 谱 可 视 化 构 建 系 统"></Header>
      <el-container>
        <Aside msg="This is aside"></Aside>
        <MainPage msg="This is main"></MainPage>
      </el-container>
    </el-container>
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'

import Header from "@/components/Header";
import Aside from './components/Aside'
import MainPage from "@/components/MainPage";

export default {
  name: 'App',
  components: {
    // HelloWorld,

    Header,
    Aside,
    MainPage
  },
  mounted() {
    this.ping();
  },
  methods: {
    ping() {
      // 使用 axios 向 flask 发送请求
      const url = "http://127.0.0.1:5000/api/ping";
      this.axios.get(url)
          .then((res) => {
            console.log(res.data);
          })
          .catch((error) => {
            console.log(error);
          })
    }

  },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;

  position: fixed;
  display: flex;
  width: 100%;
  height: 100%;
}
</style>
