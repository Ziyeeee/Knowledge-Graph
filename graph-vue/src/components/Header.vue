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
  background-color: #B3C0D1;
  color: #333;
  text-align: center;
  line-height: 80px;
}
</style>