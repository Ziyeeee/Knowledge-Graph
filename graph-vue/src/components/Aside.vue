<template>
  <el-aside width="200px">
    <el-menu
        class="el-menu-vertical-demo"\
        @select="handleSelect"
        @open="handleOpen"
        @close="handleClose">
      <el-submenu index="1">
        <template slot="title">
          <i class="el-icon-plus"></i>
          <span>添加结点</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="1-1">
            <i class="el-icon-eleme"></i>
            <span type = "" @click="AddNode1()">任务节点</span>
          </el-menu-item>
          <el-menu-item index="1-2">
            <i class="el-icon-eleme"></i>
            <span>方法结点</span>
          </el-menu-item>
          <el-menu-item index="1-3">
            <i class="el-icon-eleme"></i>
            <span>步骤结点</span>
          </el-menu-item>
          <el-menu-item index="1-4">
            <i class="el-icon-eleme"></i>
            <span>属性结点</span>
          </el-menu-item>
          <el-menu-item index="1-5">
            <i class="el-icon-eleme"></i>
            <span>概念结点</span>
          </el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <el-submenu index="2">
        <template slot="title">
          <i class="el-icon-plus"></i>
          <span slot="title">添加关系</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="2-1">
            <i class="el-icon-eleme"></i>
            <span>继承关系</span>
          </el-menu-item>
          <el-menu-item index="2-2">
            <i class="el-icon-eleme"></i>
            <span>组合关系</span>
          </el-menu-item>
          <el-menu-item index="2-3">
            <i class="el-icon-eleme"></i>
            <span>关联关系</span>
          </el-menu-item>
          <el-menu-item index="2-4">
            <i class="el-icon-eleme"></i>
            <span>属性关系</span>
          </el-menu-item>
        </el-menu-item-group>
      </el-submenu>
    </el-menu>
  </el-aside>
</template>

<script>
export default {
  name: "Aside",
  props:{
    msg:String
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    },
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    }
  }
}
</script>

<style>
  .el-aside {
    background-color: #E1B2B1;
    color: #824D56;
    text-align: left;
    width: 20px;
  }
  .el-menu-item-group{
    background-color: #eeeeee;
    color: #824D56;
  }
  .el-submenu{
    background-color: #dddddd;
    color: #824D56;
  }
</style>