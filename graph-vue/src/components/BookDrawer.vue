<template>
  <el-drawer id="drawer"
    title="原文参考"
    :visible.sync="drawer"
    :modal="false"
    :show-close="true"
    :before-close="handleClose">
    <Chap18></Chap18>
  </el-drawer>
</template>

<script>
  import Chap18 from "@/assets/textbook/Chap18";
  export default {
    name: "BookDrawer",
    props: {
      drawer: Boolean,
      selectedNode: Object,
    },
    components: {Chap18},
    data() {
      return {
        drawer: false,
        selectedNode: {},
      };
    },
    watch: {
      drawer: function (newDrawer) {
        if (newDrawer == true){
          // console.log(this.drawer, this.selectedNode);
          this.editMapRow();
        }
      }
    },
    methods: {
      editMapRow() {
        this.$nextTick(() => {
          var elmnt = document.getElementById("test_img");
          console.log(elmnt);
          elmnt.scrollIntoView(true);
        })
      },
      handleClose(){
        this.$emit("isClose");
      }
    }
  }
</script>

<style>
  .el-drawer__body {
    overflow: auto;
  }

</style>