<template>
  <div>
    <GraphVue></GraphVue>
  </div>
</template>

<script>
import GraphVue from "@/components/GraphVue";

export default {
  name: "MainPage",
  props:{
    msg:String
  },
  components:{
    GraphVue
  },
  methods:{
    zoomOut: function (){
      console.log('zoomOut')
      GraphVue.methods.myZoomOut()
    },
    zoomIn: function (){
      console.log('zoomIn')
      // setZoom('zoomIn')
    }
  }
}
</script>

