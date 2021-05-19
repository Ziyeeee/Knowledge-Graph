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
        elmnt: [],
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
          this.elmnt = document.getElementsByClassName("node" + this.selectedNode.index);
          for (let i = 0; i < this.elmnt.length; i++) {
            this.elmnt[i].style.background = '#99e0fc';
          }
          this.elmnt[0].scrollIntoView(true, {behavior: "smooth"});
        })
      },
      handleClose(){
        this.$emit("isClose");
        for (let i = 0; i < this.elmnt.length; i++) {
          this.elmnt[i].style.background = '';
        }
      }
    }
  }
</script>

<style>
  .el-drawer__body {
    overflow: auto;
  }

</style>