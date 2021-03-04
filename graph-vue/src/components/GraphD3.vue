<template>
  <div>
    <svg id="GraphD3"></svg>
  </div>
</template>

<!--<script src="../assets/js/d3.v6.js"></script>-->
<script>
import * as d3 from 'd3';

var nodes = [{index: 1, label: 'Node 1'},
  {index: 2, label: 'Node 2'},
  {index: 3, label: 'Node 3'},
  {index: 4, label: 'Node 4'},
  {index: 5, label: 'Node 5'}];
var edges = [{source: 1, target: 3},
  {source: 1, target: 2},
  {source: 2, target: 4},
  {source: 2, target: 5}];

export default {
  name: "GraphD3",
  data() {
    return {
      links: [],
      gs: [],
    }
  },
  mounted() {
    this.initialGraph(nodes, edges);
  },
  methods:{
    initialGraph(nodes, edges){
      console.log(nodes);
      console.log(edges);

      var svg = d3.select("#GraphD3");

      var marge = {top:60,bottom:60,left:60,right:60};
      var width = svg.attr("width")
      var height = svg.attr("height")
      var g = svg.append("g")
          .attr("transform","translate("+marge.top+","+marge.left+")");

      var forceSimulation = d3.forceSimulation()
          .force("link",d3.forceLink())
          .force("charge",d3.forceManyBody())
          .force("center",d3.forceCenter(width/2, height/2));

      forceSimulation.nodes(nodes)
          .on("tick", this.ticked);

      forceSimulation.force("link")
          .links(edges);



      // this.links = g.append("g")
      //     .selectAll("line")
      //     .data(edges)
      //     .enter()
      //     .append("line");

      this.gs = g.selectAll(".circleText")
          .data(nodes)
          .enter()
          .append("g")
          .attr("transform",function(d){
            var cirX = d.x;
            var cirY = d.y;
            return "translate("+cirX+","+cirY+")";
          })
          // .call(d3.drag()
          //     .on("start",this.started)
          //     .on("drag",this.dragged)
          //     .on("end",this.ended)
          // );
      //绘制节点
      this.gs.append("circle")
          .attr("r",10)
      //文字
      this.gs.append("text")
          .attr("x",-10)
          .attr("y",-20)
          .attr("dy",10)
          .text(function(d){
            return d.label;
          })
    },
    ticked() {
      // this.links
      //     .attr("x1",function(d){return d.source.x;})
      //     .attr("y1",function(d){return d.source.y;})
      //     .attr("x2",function(d){return d.target.x;})
      //     .attr("y2",function(d){return d.target.y;})

      this.gs
          .attr("transform",function(d) { return "translate(" + d.x + "," + d.y + ")"; })
    }
  },
}
</script>

<style scoped>
  #GraphD3{
    width: 800px;
    height: 600px;
  }
</style>