<template>
  <el-aside width="200px">
    <el-menu
        class="el-menu-vertical-demo"
        @select="handleSelect">
      <el-submenu index="0">
        <template slot="title">
          <i class="el-icon-plus"></i>
          <span>添加节点</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="0-0">
            <i class="el-icon-eleme"></i>
            <span>任务节点</span>
          </el-menu-item>
          <el-menu-item index="0-1">
            <i class="el-icon-eleme"></i>
            <span>方法节点</span>
          </el-menu-item>
          <el-menu-item index="0-2">
            <i class="el-icon-eleme"></i>
            <span>步骤节点</span>
          </el-menu-item>
          <el-menu-item index="0-3">
            <i class="el-icon-eleme"></i>
            <span>属性节点</span>
          </el-menu-item>
          <el-menu-item index="0-4">
            <i class="el-icon-eleme"></i>
            <span>概念节点</span>
          </el-menu-item>
        </el-menu-item-group>
      </el-submenu>
      <el-menu-item class="el-submenu" index="1">
        <i class="el-icon-plus"></i>
        <span slot="title">添加关系</span>
      </el-menu-item>
      <el-menu-item class="el-submenu" index="2">
        <i class="el-icon-delete"></i>
        <span slot="title">删除节点</span>
      </el-menu-item>
      <el-menu-item class="el-submenu" index="3">
        <i class="el-icon-delete-solid"></i>
        <span slot="title">删除边</span>
      </el-menu-item>
      <el-menu-item class="el-submenu" index="4">
        <i class="el-icon-more-outline"></i>
        <span slot="title">局部展示</span>
      </el-menu-item>
    </el-menu>
  </el-aside>
</template>

<script>
export default {
  name: "Aside",
  props:{
    msg:String
  },
  data() {
    return{
      clickType: NaN,
      clickPath: undefined,
    }
  },
  methods: {
    handleSelect(key, keyPath) {
      this.$store.commit('updateClickType', keyPath);
    },
    // handleOpen(key, keyPath) {
    //
    // },
    // handleClose(key, keyPath) {
    //   console.log(key, keyPath);
    // },
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