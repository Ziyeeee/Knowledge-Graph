<template>
  <el-header height="80px">{{msg}}</el-header>
</template>

<script>
export default {
  name: "Header",
  props: {
    msg:String
  }
}
</script>

<style scoped>
.el-header{
  background-color: #E1B2B1;
  color: #824D56;
  text-align: center;
  line-height: 80px;
  font-size: 38px;
}
</style>