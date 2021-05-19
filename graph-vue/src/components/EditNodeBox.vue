<template>
  <el-dialog :visible.sync="dialogVisible" title="节点信息" :append-to-body="true" :before-close="getInfo" center>
    <el-row>
      <el-col :span="6">节点名称</el-col>
      <el-col :span="18"><el-input  :placeholder="!nodeText?'请输入节点信息':nodeText" v-model="label" @keydown.enter.native="getInfo"></el-input></el-col>
    </el-row>
    <el-row>
      <el-col :span="6">原文参考</el-col>
      <el-col :span="18"><el-input  :placeholder="!nodeRef?'请输入原文参考':nodeRef" v-model="reference" @keydown.enter.native="getInfo"></el-input></el-col>
    </el-row>
    <span slot="footer" class="dialog-footer">
      <el-button style="width: 300px" type="primary" @click="getInfo">确定</el-button>
    </span>
  </el-dialog>

</template>

<script>
export default {
  name: "EditNodeBox",
  props:{
    msg: String,
    dialogVisible: Boolean,
    nodeText: String,
    nodeRef: String,
  },
  data(){
    return{
      label:'',
      reference:'',
    }
  },
  methods:{
    getInfo(){
      const label = !this.label ? this.nodeText :this.label;
      this.label = '';
      const reference = !this.reference ? this.nodeRef :this.reference;
      this.reference = '';
      this.$emit("EditNodeInfo",label, reference);
    }
  }
}
</script>

<style scoped>
</style>