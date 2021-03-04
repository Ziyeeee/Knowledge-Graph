<template>
  <div>
    <GraphD3></GraphD3>
  </div>
</template>

<script>
import GraphD3 from "@/components/GraphD3";

export default {
  name: "MainPage",
  props:{
    msg:String
  },
  components:{
    GraphD3
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

