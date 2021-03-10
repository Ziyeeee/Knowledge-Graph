<template>
  <div id="Graph">
    <div id="GraphLayer" style="z-index: 1">
      <svg id="GraphD3"></svg>
    </div>
    <EditNodeBox id="Box" v-if="isShown" msg="This is a Box" @EditNodeInfo="EditNode"></EditNodeBox>
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
  {source: 1, target: 3},
  {source: 1, target: 4}];
const colorList = [
  '#FCFE8B',
  '#B9F385',
  '#75D6C9',
  '#BC7CDA',
  '#F385A8',
];
const opacity = 1;
const radius = 30;

export default {
  name: "GraphD3",
  components: {EditNodeBox},
  data() {
    return {
      width: 800,
      height:600,

      data: {nodes: nodes, links: edges},
      node: undefined,
      link: undefined,

      mouse: undefined,
      mouseIsSelect: false,
      cursor: undefined,
      mouseLink: undefined,

      isShown: false,
      selectedNode: {},
      selectedNodeId: NaN,

      svg: {},
      simulation: {},
      dragger: {},
    }
  },
  mounted() {
    this.initialGraph(this.data.nodes, this.data.links);
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
          .force("charge", d3.forceManyBody().strength(-1000))
          .force("link", d3.forceLink(edges).distance(radius * 5))
          .force('collide', d3.forceCollide().radius(20))
          .force("x", d3.forceX())
          .force("y", d3.forceY())
          .on("tick", this.ticked);

      this.link = this.svg.append("g")
          .selectAll("line");
      this.mouseLink = this.svg.append("g")
          .attr("stroke", "#44cef6")
          .attr("stroke-width", 3)
          .attr("stroke-dasharray", 5, 10)
          .selectAll("line");
      this.cursor = this.svg.append("circle")
          .attr("display","none")
          .attr("fill", "none")
          .attr("stroke-width", 2)
          .attr("r", radius);
      this.node = this.svg.append("g")
          .selectAll("circle");
      this.nodeText = this.svg.append("g")
          .selectAll("text");

      this.dragger = this.drag(this, this.simulation, this.mouseLink, this.data);

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
      this.selectedNode = this.data.nodes[d3.select(d.target).attr("index")];
      if (this.$store.state.clickPath && this.$store.state.clickPath[0] === "1"){
        this.cursor.attr("display", null)
            .attr("fill", colorList[this.selectedNode.groupId])
            .attr("fill-opacity", 0.2)
            .attr("stroke", colorList[this.selectedNode.groupId])
            .attr("stroke-opacity", 0.4)
            .attr("cx", this.selectedNode.x)
            .attr("cy", this.selectedNode.y)
            .transition()
            .attr("r", radius * 3);
      }
    },
    mouseLeaveNode() {
      this.mouseIsSelect = false;
      // let selectedNode = d3.select(d.target);
      if (this.$store.state.clickPath && this.$store.state.clickPath[0] === "1"){
        this.cursor.transition()
            .attr("r", radius)
            .transition()
            .attr("display", "none");
      }
    },
    clicked(event) {
      this.mouseMoved.call(this, event);
      this.addNode({x: this.mouse.x, y: this.mouse.y});
    },
    // 编辑节点信息
    Openbox(d)
    {
       this.selectedNode = this.data.nodes[d3.select(d.target).attr("index")];
       this.isShown = true;
       // d3.select("#Graph").append("div").attr("id", "BoxLayer")
       //     .append("edit_node_box")
    },
    EditNode(nodeLabel){
      this.selectedNode.label = nodeLabel;
      this.isShown = false;
      d3.select("#BoxLayer").attr("z-index", null);
      this.drawNodeText();
      console.log(this.data.nodes);
      
    },
    // 节点绘制相关
    addNode(source) {
      if(this.$store.state.clickPath && this.$store.state.clickPath[0] === "0" && !this.mouseIsSelect) {
        this.data.nodes.push({index: this.data.nodes.length, groupId: parseInt(this.$store.state.clickPath[1][2]), x: source.x, y: source.y});
        // console.log(this.data.nodes);

        this.drawNodes();

        this.simulation.nodes(this.data.nodes);
        this.simulation.alpha(1).restart();
      }
    },
    drawNodes() {
      this.node = this.node
          .data(this.data.nodes)
          .join(
              enter => enter.append("circle").attr("r", 0)
                  .attr("fill", d => colorList[d.groupId])
                  .attr("fill-opacity", opacity)
                  .attr("index", d => d.index)
                  .call(enter => enter.transition().attr("r", radius))
                  .call(this.dragger)
                  .on("mouseenter", d => this.mouseEnterNode(d))
                  .on("mouseleave", d => this.mouseLeaveNode(d))
                  .on("dblclick", d => this.Openbox(d)),
              update => update,
              exit => exit.remove()
          );
      this.drawNodeText();
    },
    drawNodeText() {
      this.nodeText = this.nodeText
          .data(this.data.nodes)
          .join(
              enter => enter.append("text")
                  .attr("id", d => d.index)
                  .attr("text-anchor","middle")
                  .text(d => d.label)
                  .call(this.dragger),
              update => update.text(d => d.label),
              exit => exit.remove()
          );
    },
    // 边绘制相关
    addLink(source, targets) {
      for (const target of targets) {
        this.data.links.push({source, target});
      }
      this.drawLinks();

      this.simulation.force("link").links(this.data.links);
      this.simulation.alpha(1).restart();
    },
    drawLinks() {
      this.link = this.link
          .data(this.data.links)
          .join(
              enter => enter.append("line").attr("stroke", "#666").attr("stroke-width", 3).attr("stroke-opacity", opacity)
          );
    },
    // 更新图
    updateGraph() {
      this.drawLinks();

      this.drawNodes();

      this.simulation.nodes(this.data.nodes);
      this.simulation.force("link").links(this.data.links);
      this.simulation.alpha(1).restart();
    },

    ticked() {
      this.node.attr("cx", d => d.x)
          .attr("cy", d => d.y);

      this.link.attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);

      this.nodeText.attr('transform', d => 'translate(' + d.x + ',' + d.y + ')');

      this.cursor.attr("cx", this.selectedNode.x)
          .attr("cy", this.selectedNode.y);
    },
    drag(self) {
      let targetNodes = [];
      function dragStarted(event) {
        // console.log(event);
        if (!event.active) self.simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
        if (self.$store.state.clickPath && self.$store.state.clickPath[0] === "1") {
          self.simulation.force("charge", null)
              .force("link", null)
              .force("x", null)
              .force("y", null);
        }
      }

      function dragged(event) {
        // console.log(event);
        event.subject.fx = event.x;
        event.subject.fy = event.y;

        if (self.$store.state.clickPath && self.$store.state.clickPath[0] === "1"){
          targetNodes = self.data.nodes.filter(node => inRange({x: event.x, y: event.y}, node)).filter(node => linkNotExist(event.subject.index, node.index))
          self.mouseLink = self.mouseLink
              .data(targetNodes)
              .join("line")
              .attr("x1", event.x)
              .attr("y1", event.y)
              .attr("x2", d => d.x)
              .attr("y2", d => d.y);
        }
      }

      function dragEnded(event) {
        if (!event.active) self.simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;

        if (self.$store.state.clickPath && self.$store.state.clickPath[0] === "1"){
          self.simulation.force("charge", d3.forceManyBody().strength(-1000))
              .force("link", d3.forceLink(self.data.links).distance(100))
              .force("x", d3.forceX())
              .force("y", d3.forceY());
          self.mouseLink = self.mouseLink
              .data([])
              .join("line");
          // console.log(event.subject.index);
          self.addLink(event.subject.index, targetNodes);
        }
      }

      function inRange({x: sx, y: sy}, {x: tx, y: ty}) {
        let distance = Math.hypot(sx - tx, sy - ty);
        return distance <= radius * 4 && distance > radius;
      }

      function linkNotExist(source, target){
        // console.log(source, target);
        let notExist = true;
        for(let i = 0, len=self.data.links.length; i < len; i++) {
          if(self.data.links[i].source.index === source && self.data.links[i].target.index === target){
            notExist = false;
          }
        }
        return notExist;
      }

      return d3.drag()
          .on("start", dragStarted)
          .on("drag", dragged)
          .on("end", dragEnded);
    },
  },
}
</script>

<style scoped>
  #GraphD3{
    width: 800px;
    height: 600px;
  }
  #Box{
    /*width: 800px;*/
    /*height: 600px;*/
    position: absolute;
    top: 50%;
    left: 50%;
    margin: -200px 0 0 -200px;
    z-index: 2;
  }
</style>