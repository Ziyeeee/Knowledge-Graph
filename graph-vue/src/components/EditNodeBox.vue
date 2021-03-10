<template>
  <el-dialog :visible.sync="dialogVisible">
      <div slot="header" class="clearfix">
        <span>节点信息</span>
      </div>
      <table id="table">
        <tr>
          <td>节点名称</td>
          <td>
            <el-input  :placeholder="!this.nodeText?'请输入节点信息':this.nodeText" v-model="label" @keydown.enter.native="getInfo"></el-input>
          </td>
        </tr>
        <tr>
          <span slot="footer" class="dialog-footer">
            <el-button style="width: 300px" type="primary" @click="getInfo">确定</el-button>
          </span>
        </tr>
      </table>
  </el-dialog>

</template>

<script>
export default {
  name: "EditNodeBox",
  props:{
    msg: String,
    dialogVisible: Boolean,
    nodeText: String,
  },
  data(){
    return{
      label:'',
    }
  },
  mounted() {
    console.log(this.dialogVisible);
  },
  methods:{
    getInfo(){
      const label = !this.label ? this.nodeText :this.label;
      this.dialogVisible = false;
      this.$emit("EditNodeInfo",label);
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