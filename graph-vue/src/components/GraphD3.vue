<template>
  <div>
    <svg id="GraphD3"></svg>
    <EditNodeBox v-if="isShown" msg="This is a Box" @EditNodeInfo="EditNode"></EditNodeBox>
  </div>
</template>

<script>
import * as d3 from 'd3';
import EditNodeBox from "@/components/EditNodeBox";

var nodes = [{index: 0, label: 'Node 1', groupId: 0},
  {index: 1, label: 'Node 2', groupId: 1},
  {index: 2, label: 'Node 3', groupId: 2},
  {index: 3, label: 'Node 4', groupId: 3},
  {index: 4, label: 'Node 5', groupId: 4}];
var edges = [{source: 0, target: 2},
  {source: 0, target: 1},
  {source: 1, target: 3},
  {source: 1, target: 4}];
const colorList = [
  '#FCFE8B',
  '#B9F385',
  '#75D6C9',
  '#BC7CDA',
  '#F385A8',
];
const opacity = 0.8;

export default {
  name: "GraphD3",
  data() {
    return {
      width: 800,
      height:600,

      node: [],
      link: [],

      mouse: null,
      mouseIsSelect: false,

      isShown: false,
      selectedId: NaN,

      svg: {},
      simulation: {},
      dragger: {},
    }
  },
  components:{
    EditNodeBox
  },
  mounted() {
    this.initialGraph(nodes, edges);
  },
  methods:{
    // 初始化图
    initialGraph(nodes, edges){
      this.svg = d3.select("#GraphD3")
          .attr("viewBox", [-this.width / 2, -this.height / 2, this.width, this.height])
          .on("mouseleave", this.mouseLeft)
          .on("mousemove", this.mouseMoved)
          .on("click", this.clicked)
          .on("dbcklick", this.addInfo);

      this.simulation = d3.forceSimulation(nodes)
          .force("charge", d3.forceManyBody().strength(-800))
          .force("link", d3.forceLink(edges).distance(100))
          .force('collide', d3.forceCollide().radius(20))
          .force("x", d3.forceX())
          .force("y", d3.forceY())
          .on("tick", this.ticked);

      this.dragger = this.drag(this.simulation);

      this.link = this.svg.append("g")
          .selectAll("line");
      this.node = this.svg.append("g")
          .selectAll("circle");
      this.nodetext = this.svg.append("g")
          .selectAll("text");

      this.updateGraph();
    },
    // 鼠标事件
    mouseLeft() {
      this.mouse = null;
    },
    mouseMoved(event) {
      const [x, y] = d3.pointer(event);
      this.mouse = {x, y};
      // this.simulation.alpha(0.3).restart();
    },
    mouseEnterNode(d) {
      this.mouseIsSelect = true;
      d3.select(d.target).attr("fill-opacity", 1);
    },
    mouseLeaveNode(d) {
      this.mouseIsSelect = false;
      d3.select(d.target).attr("fill-opacity", 0.8);
    },
    clicked(event) {
      this.mouseMoved.call(this, event);
      this.addNode({x: this.mouse.x, y: this.mouse.y});
    },
    // 编辑节点
    Openbox(d)
    {
       this.selectedId = d3.select(d.target).attr("index");
       this.isShown = true;
    },
    EditNode(text){
      nodes[this.selectedId].label = text;
      this.isShown = false;
      // console.log(nodes);
    },
    // 节点绘制相关
    addNode(source) {
      if(this.$store.state.clickPath && this.$store.state.clickPath[0] == "0" && !this.mouseIsSelect) {
        nodes.push({index: nodes.length, groupId: parseInt(this.$store.state.clickPath[1][2]), x: source.x, y: source.y});
        // console.log(nodes);

        this.drawNodes();

        this.simulation.nodes(nodes);
        this.simulation.alpha(1).restart();
      }
    },
    drawNodes() {
      this.node = this.node
          .data(nodes)
          .join(
              enter => enter.append("circle").attr("r", 0)
                  .attr("fill", d => colorList[d.groupId])
                  .attr("fill-opacity", opacity)
                  .attr("index", d => d.index)
                  .call(enter => enter.transition().attr("r", 20))
                  .call(this.dragger)
                  .on("mouseenter", d => this.mouseEnterNode(d))
                  .on("mouseleave", d => this.mouseLeaveNode(d))
                  .on("dblclick", d => this.Openbox(d)),
              update => update,
              exit => exit.remove()
          );
      this.nodetext = this.nodetext
          .data(nodes)
          .join(
              enter => enter.append("text").attr("text-anchor","middle")
                  .text(function (d){
                    return d.label
                  })
                  .call(this.dragger),
              update => update,
              exit => exit.remove()
          );
    },
    // 边绘制相关
    addLink() {
      this.drawLinks();

      this.simulation.force("link").links(edges);
      this.simulation.alpha(1).restart();
    },
    drawLinks() {
      this.link = this.link
          .data(edges)
          .join(
              enter => enter.append("line").attr("stroke", "#666").attr("stroke-width", 3).attr("stroke-opacity", opacity)
          );
    },
    // 更新图
    updateGraph() {
      this.drawLinks();

      this.drawNodes();

      this.simulation.nodes(nodes);
      this.simulation.force("link").links(edges);
      this.simulation.alpha(1).restart();
    },

    ticked() {
      this.node.attr("cx", d => d.x)
          .attr("cy", d => d.y)

      this.link.attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);

      this.nodetext.attr('transform', function(d) {
        return 'translate(' + d.x + ',' + d.y + ')';
      });
    },
    drag(simulation) {
      function dragStarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
      }

      function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
      }

      function dragEnded(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
      }

      return d3.drag()
          .on("start", dragStarted)
          .on("drag", dragged)
          .on("end", dragEnded);
    },
    // inRange({x: sx, y: sy}, {x: tx, y: ty}) {
    //   return Math.hypot(sx - tx, sy - ty) <= this.minDistance;
    // },
  },
}
</script>

<style scoped>
  #GraphD3{
    width: 800px;
    height: 600px;
  }
</style>