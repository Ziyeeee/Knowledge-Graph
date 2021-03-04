<template>
  <div>
    <svg id="GraphD3"></svg>
  </div>
</template>

<!--<script src="../assets/js/d3.v6.js"></script>-->
<script>
import * as d3 from 'd3';

var nodes = [{index: 0, label: 'Node 1'},
  {index: 1, label: 'Node 2'},
  {index: 2, label: 'Node 3'},
  {index: 3, label: 'Node 4'},
  {index: 4, label: 'Node 5'}];
var edges = [{source: 0, target: 2},
  {source: 0, target: 1},
  {source: 1, target: 3},
  {source: 1, target: 4}];
// var nodes = [];
// var edges = [];

export default {
  name: "GraphD3",
  data() {
    return {
      minDistance: 30,
      width: 800,
      height:600,

      node: [],
      link: [],

      mouseLink: [],
      cursor: {},
      mouse: null,

      svg: {},
      simulation: {},
      dragger: {},
    }
  },
  mounted() {
    this.initialGraph(nodes, edges);
  },
  methods:{
    initialGraph(nodes, edges){
      this.svg = d3.select("#GraphD3")
          .property("value", {nodes: nodes, links: edges})
          .attr("viewBox", [-this.width / 2, -this.height / 2, this.width, this.height])
          // .attr("cursor", "crosshair")
          .on("mouseleave", this.mouseLeft)
          .on("mousemove", this.mouseMoved)
          .on("click", this.clicked);

      this.simulation = d3.forceSimulation(nodes)
          .force("charge", d3.forceManyBody().strength(-60))
          .force("link", d3.forceLink(edges))
          .force("x", d3.forceX())
          .force("y", d3.forceY())
          .on("tick", this.ticked);

      this.dragger = d3.drag(this.simulation)
          .on("start.mouse", this.mouseLeft)
          .on("end.mouse", this.mouseMoved);

      this.link = this.svg.append("g")
          .attr("stroke", "#999")
          .selectAll("line");

      this.mouselink = this.svg.append("g")
          .attr("stroke", "red")
          .selectAll("line");

      this.node = this.svg.append("g")
          .selectAll("circle");

      this.cursor = this.svg.append("circle")
          .attr("display", "none")
          .attr("fill", "none")
          .attr("stroke", "red")
          .attr("r", this.minDistance - 5);

      this.spawn({x: 0, y: 0});
    },
    ticked() {
      this.node.attr("cx", d => d.x)
          .attr("cy", d => d.y)

      this.link.attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);

      this.mouselink = this.mouselink
          .data(this.mouse ? nodes.filter(node => this.inRange(this.mouse, node)) : [])
          .join("line")
          .attr("x1", this.mouse && this.mouse.x)
          .attr("y1", this.mouse && this.mouse.y)
          .attr("x2", d => d.x)
          .attr("y2", d => d.y);

      this.cursor
          .attr("display", this.mouse ? null : "none")
          .attr("cx", this.mouse && this.mouse.x)
          .attr("cy", this.mouse && this.mouse.y);
    },
    mouseLeft() {
      this.mouse = null;
    },
    inRange({x: sx, y: sy}, {x: tx, y: ty}) {
      return Math.hypot(sx - tx, sy - ty) <= this.minDistance;
    },
    mouseMoved(event) {
      const [x, y] = d3.pointer(event);
      this.mouse = {x, y};
      this.simulation.alpha(0.3).restart();
    },
    clicked(event) {
      this.mouseMoved.call(this, event);
      this.spawn({x: this.mouse.x, y: this.mouse.y});
    },
    spawn(source) {
      nodes.push(source);

      for (const target of nodes) {
        if (this.inRange(source, target)) {
          edges.push({source, target});
        }
      }

      this.link = this.link
          .data(edges)
          .join("line");

      this.node = this.node
          .data(nodes)
          .join(
              enter => enter.append("circle").attr("r", 0)
                  .call(enter => enter.transition().attr("r", 5))
                  .call(this.dragger),
              update => update,
              exit => exit.remove()
          );

      this.simulation.nodes(nodes);
      this.simulation.force("link").links(edges);
      this.simulation.alpha(1).restart();

      this.svg.property("value", {
        nodes: nodes.map(d => ({id: d.index})),
        links: edges.map(d => ({source: d.source.index, target: d.target.index}))
      });

      this.svg.dispatch("input");
    },
  },
}
</script>

<style scoped>
  #GraphD3{
    width: 800px;
    height: 600px;
  }
</style>