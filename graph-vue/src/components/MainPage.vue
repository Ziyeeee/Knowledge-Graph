<template>
  <div>
<!--    <GraphVue></GraphVue>-->
    <GraphVis></GraphVis>
  </div>
</template>

<script>
// import GraphVue from "@/components/GraphVue";
import GraphVis from "@/components/GraphVis";

export default {
  name: "MainPage",
  props:{
    msg:String
  },
  components:{
    // GraphVue
    GraphVis
  },
  methods:{
    // zoomOut: function (){
    //   console.log('zoomOut')
    //   GraphVue.methods.myZoomOut()
    // },
    // zoomIn: function (){
    //   console.log('zoomIn')
    //   // setZoom('zoomIn')
    // }
  }
}
</script>

