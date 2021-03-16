<template>
  <div id="Graph">
    <div id="GraphLayer" style="">
      <svg id="GraphD3"></svg>
    </div>

    <div id="SetBar">
      <el-button><i class="el-icon-refresh-left"> 撤销</i></el-button>
      <el-button><i class="el-icon-refresh-right"> 恢复</i></el-button>
      <el-button><i class="el-icon-folder" @click="this.saveGraph"> 保存</i></el-button>
      <el-button @click="zoomIn"><i class="el-icon-zoom-in"></i> 放大</el-button>
      <el-button @click="zoomOut"><i class="el-icon-zoom-out"></i> 缩小</el-button>
      <el-button @click="refresh"><i class="el-icon-refresh-right"></i> 还原</el-button>
      <el-button v-if="!isFullScreen" @click="showFullScreen"><i class="el-icon-full-screen"></i> 全屏</el-button>
      <el-button v-else @click="exitFullScreen" @keyup.space="exitFullScreen"><i class="el-icon-full-screen"></i> 退出全屏</el-button>
    </div>
    <EditNodeBox id="EditNodeBox" :dialogVisible="this.isVisible" msg="This is a Box" :nodeText="this.selectedNode.label" @EditNodeInfo="EditNode"></EditNodeBox>

  </div>
</template>

<script>
import * as d3 from 'd3';
import EditNodeBox from "@/components/EditNodeBox";


// var nodes = [{index: 0, label: 'Node 1', groupId: 0},
//   {index: 1, label: 'Node 2', groupId: 1},
//   {index: 2, label: 'Node 3', groupId: 2},
//   {index: 3, label: 'Node 4', groupId: 3},
//   {index: 4, label: 'Node 5', groupId: 4}];
// var edges = [{source: 0, target: 2},
//   {source: 0, target: 1},
//   {source: 1, target: 3},
//   {source: 1, target: 3},
//   {source: 1, target: 4}];

const colorList = [
  '#FCFE8B',
  '#B9F385',
  '#75D6C9',
  '#bc7cda',
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
      zoom: null,
      isFullScreen: false,
      isVisible: false,
      timer: false,

      data: {},
      // data: {nodes: nodes, links: edges},
      node: undefined,
      link: undefined,
      arrow: undefined,

      mouse: undefined,
      mouseIsSelect: false,
      cursor: undefined,
      mouseLink: undefined,

      isShown: false,
      selectedNode: {},
      selectedEdge: {},
      cursorNode: {},

      svg: {},
      simulation: {},
      dragger: {},
    }
  },
  mounted() {
  //解决esc键无法触发事件
    let that = this;
    this.setGraphWindow();
    window.onresize = function(){
      if(!that.checkFull()){
        that.isFullScreen = false;
      }
      if(!that.timer){ // 使用节流机制，降低函数被触发的频率
        that.timer = true;
        setTimeout(function(){
          that.setGraphWindow();
          that.timer = false;
        },400)
      }
    };

    this.initialGraph();
  },
  methods:{
    // 初始化图
    initialGraph(){
      const url = "http://127.0.0.1:5000/api/get_data";
      this.axios.get(url)
          .then((res) => {
            this.data = res.data;
            console.log(res.data);
            this.svg = d3.select("#GraphD3")
                .attr("height", this.height)
                .attr("width", this.width)
                .attr("viewBox", [-this.width / 2, -this.height / 2, this.width, this.height])
                .on("mouseleave", this.mouseLeft)
                .on("mousemove", this.mouseMoved)
                .on("click", this.clicked)
                .on("dbcklick", this.addInfo);

            this.simulation = d3.forceSimulation(this.data.nodes)
                .force("charge", d3.forceManyBody().strength(-1000))
                .force("link", d3.forceLink(this.data.links).distance(radius * 5))
                .force('collide', d3.forceCollide().radius(radius))
                .force("x", d3.forceX())
                .force("y", d3.forceY())
                .on("tick", this.ticked);

            this.node = this.svg.append("g")
                .selectAll("circle");
            this.link = this.svg.append("g")
                .selectAll("line");
            this.nodeText = this.svg.append("g")
                .selectAll("text");
            this.arrowMaker = this.svg.append("defs").append("marker")
                .attr("id", "arrow")
                .attr("markerUnits","strokeWidth")
                .attr("markerWidth", "8")
                .attr("markerHeight", "8")
                .attr("refX","9")
                .attr("refY","6")
                .attr("viewBox","0 0 12 12")
                .attr('orient', 'auto')
                .append("path")
                .attr("d", "M2,2 L10,6 L2,10 L6,6 L2,2")
                .attr("fill", "#999")
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

            this.dragger = this.drag(this, this.simulation, this.mouseLink, this.data);
            
            this.zoom = d3.zoom().extent([[0, 0], [this.width, this.height]]).scaleExtent([0.1, 4]).on("zoom", this.zoomed);
            this.svg.call(this.zoom);
            this.svg.on("dblclick.zoom",null);
            
            this.updateGraph();
          })
          .catch((error) => {
            console.log(error);
          })
    },

    setGraphWindow() {
      this.height = window.innerHeight-80;
      this.width = window.innerWidth-200;
      // console.log(this.height, this.width);
      this.svg = d3.select("#GraphD3")
          .attr("height", this.height)
          .attr("width", this.width)
          .attr("viewBox", [-this.width / 2, -this.height / 2, this.width, this.height])
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
      this.cursorNode = this.selectedNode;
      if (this.$store.state.clickPath && this.$store.state.clickPath[0] === "1"){
        this.cursorNode = this.selectedNode;
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
      if (this.$store.state.clickPath && this.$store.state.clickPath[0] === "2"){
        this.cursorNode = this.selectedNode;
        this.cursor.attr("display", null)
            .attr("fill", "#696969")
            .attr("fill-opacity", 0.2)
            .attr("stroke", "#696969")
            .attr("stroke-opacity", 0.4)
            .attr("cx", this.selectedNode.x)
            .attr("cy", this.selectedNode.y)
            .transition()
            .attr("r", radius * 1.5);
      }
    },
    mouseLeaveNode(d) {
      this.mouseIsSelect = false;
      if (this.$store.state.clickPath && (this.$store.state.clickPath[0] === "1" || this.$store.state.clickPath[0] === "2")){
        this.cursor.transition()
            .attr("r", radius)
            .transition()
            .attr("display", "none")
            .on('end', function (){this.cursorNode = {}})
      }
      this.selectedNode = {};
    },
    mouseEnterEdge(d){
      if(this.$store.state.clickPath && this.$store.state.clickPath[0] === "3"){
        this.mouseIsSelect = true;
        this.selectedEdge = this.data.links[d3.select(d.target).attr("index")];
        d3.select(d.target).transition()
            .attr("stroke-width", 8);
      }

    },
    mouseLeaveEdge(d){
      this.mouseIsSelect = false;
      this.selectedEdge = {};
      d3.select(d.target).transition()
          .attr("stroke-width", 3);
    },
    clicked(event) {
      if(this.$store.state.clickPath && this.$store.state.clickPath[0] === "0"){
        this.mouseMoved.call(this, event);
        this.addNode({x: this.mouse.x, y: this.mouse.y});
      }
      if(this.$store.state.clickPath && this.$store.state.clickPath[0] === "2"){
        this.deleteNode();
      }
      if(this.$store.state.clickPath && this.$store.state.clickPath[0] === "3"){
        this.deleteLink();
      }
    },

    // 编辑节点信息
    Openbox(d)
    {
       this.selectedNode = this.data.nodes[d3.select(d.target).attr("index")];
       this.isVisible = true;
    },
    EditNode(nodeLabel){
      this.selectedNode.label = nodeLabel;
      this.drawNodeText();
      this.isVisible = false;
    },

    saveGraph(){
      const url = "http://127.0.0.1:5000/api/post_data";
      const data = {nodes: this.data.nodes, links: this.data.links}
      console.log(data)
      this.axios.post(url, data)
          .then((res) => console.log(res.data))
          .catch((error) => console.log(error))
    },

    // 节点绘制相关
    addNode(source) {
      if(!this.mouseIsSelect) {
        this.data.nodes.push({index: this.data.nodes.length, groupId: parseInt(this.$store.state.clickPath[1][2]), x: source.x, y: source.y});
        // console.log(this.data.nodes);

        this.drawNodes();

        this.simulation.nodes(this.data.nodes);
        this.simulation.alpha(1).restart();
      }
    },

    deleteNode(){
      if(this.mouseIsSelect){
        this.data.links = this.data.links.filter(item => !(item.source.index === this.selectedNode.index || item.target.index === this.selectedNode.index));
        this.data.nodes.splice(this.selectedNode.index, 1);
        this.mouseLeaveNode();
        this.updateGraph();
      }
    },
    drawNodes() {
      this.node = this.node
          .data(this.data.nodes)
          .join(
              enter => enter.append("circle")
                  .attr("r", 0)
                  .attr("fill", d => colorList[d.groupId])
                  .attr("fill-opacity", opacity)
                  .attr("index", d => d.index)
                  .call(enter => enter.transition().attr("r", radius))
                  .call(this.dragger)
                  .on("mouseenter", d => this.mouseEnterNode(d))
                  .on("mouseleave", d => this.mouseLeaveNode(d))
                  .on("dblclick", d => this.Openbox(d)),
              update => update.attr("fill", d => colorList[d.groupId]),
              exit => exit.remove()
          );
      this.drawNodeText();
    },
    drawNodeText() {
      this.nodeText = this.nodeText
          .data(this.data.nodes)
          .join(
              enter => enter.append("text")
                  .attr("index", d => d.index)
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
    deleteLink(){
      if(this.mouseIsSelect) {
        this.data.links.splice(this.selectedEdge.index, 1);
        this.updateGraph();
      }
    },
    drawLinks() {
      this.link = this.link
          .data(this.data.links)
          .join(
              enter => enter.append("line")
                  .attr("stroke", "#999")
                  .attr("stroke-width", 3)
                  .attr("stroke-opacity", opacity)
                  .attr("marker-end", "url(#arrow)")
                  .attr("index", d => d.index)
                  .on("mouseenter", d => this.mouseEnterEdge(d))
                  .on("mouseleave",d => this.mouseLeaveEdge(d)),
              update => update,
              exit => exit.remove()
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

      this.link.attr("x1", d => d.source.x - offsetX(d))
          .attr("y1", d => d.source.y - offsetY(d))
          .attr("x2", d => d.target.x + offsetX(d))
          .attr("y2", d => d.target.y + offsetY(d));

      this.nodeText.attr('transform', d => 'translate(' + d.x + ',' + d.y + ')');

      this.cursor.attr("cx", this.cursorNode.x)
          .attr("cy", this.cursorNode.y);

      function offsetX(d){
        return radius * (d.source.x - d.target.x) / Math.hypot(d.source.x-d.target.x, d.source.y-d.target.y)
      }
      function offsetY(d){
        return radius * (d.source.y - d.target.y) / Math.hypot(d.source.x-d.target.x, d.source.y-d.target.y)
      }
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

    //编辑视图相关
    zoomed({transform}) {
      d3.selectAll("g").attr("transform", transform);
     },
    zoomClick(direction) {
      var factor = 0.2
      var targetZoom = 1
      var extent = this.zoom.scaleExtent()
      targetZoom = 1 + factor * direction
      if (targetZoom < extent[0] || targetZoom > extent[1]) {
        return false}
      this.zoom.scaleBy(this.svg, targetZoom) // 执行该方法后 会触发zoom事件
    },
    zoomIn() {
      this.zoomClick(1)
    },
    zoomOut() {
      this.zoomClick(-1)
    },
    refresh() {
      this.svg.call(this.zoom.transform, d3.zoomIdentity)
    },
    checkFull() {
      var isFull = document.mozFullScreen ||
          document.fullScreen ||
          document.webkitIsFullScreen ||
          document.webkitRequestFullScreen ||
          document.mozRequestFullScreen ||
          document.msFullscreenEnabled
      if (isFull === undefined) {
        isFull = false
      }
      return isFull;
    },
    showFullScreen(){
      this.isFullScreen = true;
      var element = document.getElementById("Graph");
      if (element.requestFullscreen) {
        element.requestFullscreen()
      } else if (element.mozRequestFullScreen) {
        element.mozRequestFullScreen()
      } else if (element.webkitRequestFullscreen) {
        element.webkitRequestFullscreen()
      } else if (element.msRequestFullscreen) {
        element.msRequestFullscreen()
      }
    },
    exitFullScreen(){
      this.isFullScreen = false;
      if (document.exitFullscreen) {
        document.exitFullscreen()
      } else if (document.mozCancelFullScreen) {
        document.mozCancelFullScreen()
      } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen()
      }
    },
  },

}
</script>

<style scoped>
  /*#GraphD3{*/
  /*  width: 800px;*/
  /*  height: 600px;*/
  /*}*/
  #GraphLayer{
    z-index: 1;
    /*border:6px solid #2196F3;*/
    /*background-color: #ddffff;*/
  }
  #SetBar{
    position: absolute;
    top: 80px;
    left: 200px;
    margin: 10px;
  }
</style>