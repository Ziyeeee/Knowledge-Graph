<template>
  <div id="app">
    <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    <!-- <GraphVue></GraphVue>-->
    <el-container v-if="$route.meta.keepalive" direction="vertical">
        <Header msg="This is a header"></Header>
      <el-container>
        <Aside msg="This is aside"></Aside>
        <MainPage msg="This is main"></MainPage>
      </el-container>

    </el-container>
    <router-view v-if="!$route.meta.keepalive"></router-view>
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
    MainPage,
  }
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
