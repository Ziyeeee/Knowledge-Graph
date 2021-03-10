<template>
  <div id="box">
    <el-card id="card" style="width: 400px; height: 200px">
      <div slot="header" class="clearfix">
        <span>节点信息</span>
      </div>
      <table id="table">
        <tr>
          <td>节点名称</td>
          <td>
            <el-input placeholder="请输入节点名称" v-model="label" @keydown.enter.native="getInfo"></el-input>
          </td>
        </tr>
        <tr>
          <td colspan="2">
            <el-button style="width: 300px" type="primary" @click="getInfo">确定</el-button>
          </td>
        </tr>
      </table>
    </el-card>
  </div>

</template>

<script>
export default {
  name: "EditNodeBox",
  props:{
    msg: String
  },
  data(){
    return{
      label:'',
    }
  },
  methods:{
    getInfo(){
      const label = this.label;
      console.log(label);
      this.$emit("EditNodeInfo",this.label);
    }
  }
}
</script>

<style scoped>
  #box{
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
</style>