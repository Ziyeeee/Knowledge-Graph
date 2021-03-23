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
  background-color: #99BCD6;
  color: #032946;
  text-align: center;
  line-height: 80px;
  font-size: 38px;
}
</style>