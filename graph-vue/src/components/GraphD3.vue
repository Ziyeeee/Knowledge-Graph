<template>
  <div id="Graph">
    <div id="GraphLayer" style="">
      <svg id="GraphD3"></svg>
    </div>
    <div id="SetBar">
      <el-row>
        <el-col :span="12">
          <el-button><i class="el-icon-folder" @click="this.saveGraph"> 保存</i></el-button>
          <el-button @click="zoomIn"><i class="el-icon-zoom-in"></i> 放大</el-button>
          <el-button @click="zoomOut"><i class="el-icon-zoom-out"></i> 缩小</el-button>
          <el-button @click="refresh"><i class="el-icon-refresh-right"></i> 还原</el-button>
          <el-button v-if="!isFullScreen" @click="showFullScreen"><i class="el-icon-full-screen"></i> 全屏</el-button>
          <el-button v-else @click="exitFullScreen" @keyup.space="exitFullScreen"><i class="el-icon-full-screen"></i> 退出全屏</el-button>
        </el-col>
        <el-col :span="12">
          <el-autocomplete
              class="inline-input"
              v-model="searchInput"
              :fetch-suggestions="searchAutoComplete"
              placeholder="搜索"
              @select="handleSelect"
          >
            <el-button slot="append" icon="el-icon-search" @click="findSubGraph"  ></el-button>
          </el-autocomplete>
<!--          <el-input v-model="searchInput" clearable placeholder="搜索" @keydown.enter.native="findSubGraph">-->
<!--            <el-button slot="append" icon="el-icon-search" @click="findSubGraph"></el-button>-->
<!--          </el-input>-->
        </el-col>
      </el-row>
    </div>
    <el-dialog :title="cardTitle" :visible.sync="dialogCardVisible" :append-to-body="true">
      <el-card class="box-card" shadow="never">
        <div v-for="item in cardItems" :key="item" class="text item">
          <el-card shadow="hover">
            <el-link type="primary" align="left" @click="clickCardText(item.label)" >{{item.label}}</el-link>
            <el-divider><i class="el-icon-s-management"></i></el-divider>
            <el-col align="left">原文参考：{{item.reference}}<br /><br /></el-col>
          </el-card>
        </div>
      </el-card>
    </el-dialog>
    <EditNodeBox id="EditNodeBox" :nodeText="this.selectedNode.label" :nodeRef="this.selectedNode.reference" :dialogVisible="this.isVisible"  msg="This is a Box"  @EditNodeInfo="EditNode"></EditNodeBox>
    <BookDrawer :drawer="this.isShowDrawer" :selected-node="this.selectedNode" :indexNew2Old="this.indexNew2Old" @isClose="closeDrawer"></BookDrawer>
  </div>
</template>

<script>
import * as d3 from 'd3';
import EditNodeBox from "@/components/EditNodeBox";
import BookDrawer from "@/components/BookDrawer";

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
  '#BC7CDA',
  '#F385A8',
];
const opacity = 1;
const radius = 30;

export default {
  name: "GraphD3",
  components: {BookDrawer, EditNodeBox},
  props:{
    isShowMainGraph: Boolean
  },
  data() {
    return {
      width: 800,
      height:600,
      zoom: null,
      isFullScreen: false,
      isVisible: false,
      timer: false,
      searchInput: '',
      autoCompleteList: [],
      selectAutoComplete: {},
      isRecommendQuery: false,
      dialogCardVisible: false,
      cardTitle: '',
      cardItems: [],
      isShowDrawer: false,
      indexNew2Old: [],

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
  watch:{
    isShowMainGraph: function (newFlag, oldFlag){
      if(newFlag) {
        this.showMainGraph()
      }
    }
  },
  methods:{
    // 初始化图
    initialGraph(){
      const url = "http://127.0.0.1:5000/api/get_data";
      this.axios.get(url)
          .then((res) => {
            this.data = res.data;
            this.indexNew2Old = [];
            console.log(res.data);
            this.svg = d3.select("#GraphD3")
                .attr("height", this.height)
                .attr("width", this.width)
                .attr("viewBox", [-this.width / 2, -this.height / 2, this.width, this.height])
                .on("mouseleave", this.mouseLeft)
                .on("mousemove", this.mouseMoved)
                .on("click", this.clicked);

            this.simulation = d3.forceSimulation(this.data.nodes)
                .force("charge", d3.forceManyBody().strength(-2000))
                .force("link", d3.forceLink(this.data.links).distance(radius * 5))
                .force('collide', d3.forceCollide().radius(radius))
                .force("x", d3.forceX())
                .force("y", d3.forceY())
                .on("tick", this.ticked);

            this.cursor = this.svg.append('g')
                .append("circle")
                .attr("display","none")
                .attr("fill", "none")
                .attr("stroke-width", 2)
                .attr("r", radius);
            this.link = this.svg.append("g")
                .selectAll("path");
            this.mouseLink = this.svg.append("g")
                .selectAll("line");
            this.node = this.svg.append("g")
                .selectAll("circle");
            this.nodeText = this.svg.append("g")
                .selectAll("text");
            this.svg.append("defs").append("marker")
                .attr("id", "arrow")
                .attr("markerUnits","userSpaceOnUse")
                .attr("viewBox", "0 0 12 12")
                .attr("refX", 10)
                .attr("refY", 6)
                .attr("markerWidth", 26)//标识的大小
                .attr("markerHeight", 26)
                .attr("orient", "auto")//绘制方向，可设定为：auto（自动确认方向）和 角度值
                .attr("stroke-width",2)//箭头宽度
                .append("path")
                .attr("d", "M2,2 L10,6 L2,10 L6,6 L2,2")//箭头的路径
                .attr('fill',"#666");//箭头颜色

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
      if (this.$store.state.clickPath){
        if(this.$store.state.clickPath[0] !== "3") this.mouseIsSelect = true;
        if(this.$store.state.clickPath[0] === "1"){
          this.selectedNode = this.data.nodes[d3.select(d.target).attr("index")];
          this.cursorNode = this.selectedNode;
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
        else if(this.$store.state.clickPath[0] === "2"){
          this.selectedNode = this.data.nodes[d3.select(d.target).attr("index")];
          this.cursorNode = this.selectedNode;
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
        else if(this.$store.state.clickPath[0] === "4" || this.$store.state.clickPath[0] === "6") {
          this.selectedNode = this.data.nodes[d3.select(d.target).attr("index")];
          this.cursorNode = this.selectedNode;
          this.cursorNode = this.selectedNode;
          this.cursor.attr("display", null)
              .attr("fill", colorList[this.selectedNode.groupId])
              .attr("fill-opacity", 0.2)
              .attr("stroke", colorList[this.selectedNode.groupId])
              .attr("stroke-opacity", 0.4)
              .attr("cx", this.selectedNode.x)
              .attr("cy", this.selectedNode.y)
              .transition()
              .attr("r", radius * 1.5);
        }
      }
    },
    // eslint-disable-next-line no-unused-vars
    mouseLeaveNode(d) {
      this.mouseIsSelect = false;
      if (this.$store.state.clickPath && (this.$store.state.clickPath[0] === "1" ||
          this.$store.state.clickPath[0] === "2" ||this.$store.state.clickPath[0] === "4"||
          this.$store.state.clickPath[0] === "6")){
        this.cursor.transition()
            .attr("r", radius)
            .transition()
            .attr("display", "none")
            .on('end', function (){this.cursorNode = {}})
        // this.selectedNode = {};
      }

    },
    mouseEnterEdge(d){
      if(this.$store.state.clickPath && this.$store.state.clickPath[0] === "3"){
        this.mouseIsSelect = true;
        this.selectedEdge = this.data.links[d3.select(d.target).attr("index")];
        d3.select(d.target).transition()
            .attr("stroke-width", 8);
        // console.log(d.target, d3.select(d.target))
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
      if(this.$store.state.clickPath && this.$store.state.clickPath[0] === "4"){
        this.getSubGraph();
      }
      if(this.$store.state.clickPath && this.$store.state.clickPath[0] === "6"){
        this.openDrawer();
      }
    },

    //保存
    saveGraph(){
      const url = "http://127.0.0.1:5000/api/post_data";
      const data = {nodes: this.data.nodes, links: this.data.links}
      console.log(data)
      this.axios.post(url, data)
          .then((res) => {
            if(res.data) {
              this.$message({
                message: '保存成功',
                type: 'success'
              });
            }
          })
          .catch((error) => console.log(error))
    },

    getSubGraph(){
      const url = "http://127.0.0.1:5000/api/get_subGraphData";
      this.axios.get(url, {params: {baseNodeIndex: this.selectedNode.index, numLayer: 3}})
          .then((res) => {
            this.mouseLeaveNode();
            console.log(res.data);
            this.data = res.data.subgraph;
            this.indexNew2Old = res.data.new2old;
            this.updateGraph();
          })
          .catch((error) =>{
            console.log(error)
          })
    },

    findSubGraph(){
      const url = "http://127.0.0.1:5000/api/get_search";
      this.axios.get(url, {params: {search: this.searchInput, numLayer: 3, isRecommend: this.isRecommendQuery}})
          .then((res) => {
            console.log(res.data);
            if(res.data == false) {
              this.$message({
                message: '未找到相关信息',
                type: 'warning'
              });
            }
            else {
              this.data = res.data.subgraph;
              this.indexNew2Old = res.data.new2old;
              this.updateGraph();
              if (this.isInList(this.searchInput, this.autoCompleteList)){
                this.dialogCardVisible = true
                this.cardTitle = this.searchInput
                this.cardItems = this.data.nodes.slice(1)
              }
            }
          })
          .catch((error) =>{
            console.log(error)
          })
    },

    searchAutoComplete(queryString, cb){
      // console.log(queryString)

      if (!this.isInList(queryString, this.autoCompleteList)){
        this.isRecommendQuery = false
        const url = "http://127.0.0.1:5000/api/get_autoComplete";
        this.axios.get(url, {params: {search: this.searchInput}})
            .then((res) => {
              // console.log(res.data);
              // this.data = res.data;
              this.autoCompleteList = res.data;
              cb(res.data);
            })
            .catch((error) =>{
              console.log(error);
            })
      }
      else {
        cb([]);
      }
    },

    handleSelect() {
      this.isRecommendQuery = true;
    },

    isInList(value, list){
      for(let i=0; i < list.length; i++){
        if(value === list[i]['value']){
          return true;
        }
      }
      return false;
    },

    clickCardText(text){
      this.searchInput = text;
      const url = "http://127.0.0.1:5000/api/get_search";
      this.axios.get(url, {params: {search: text, numLayer: 3, isRecommend: false}})
          .then((res) => {
            console.log(res.data);
            if(res.data == false) {
              this.$message({
                message: '未找到相关信息',
                type: 'warning'
              });
            }
            else {
              this.data = res.data.subgraph;
              this.indexNew2Old = res.data.new2old;
              this.updateGraph();
            }
          })
          .catch((error) =>{
            console.log(error)
          })
      this.dialogCardVisible = false;
    },

    showMainGraph(){
      // console.log(this.isShowMainGraph, this.$store.state.showMainGraph)
      const url = "http://127.0.0.1:5000/api/get_mainGraphData";
      this.axios.get(url)
          .then((res) => {
            // console.log(res.data);
            this.data = res.data;
            this.indexNew2Old = [];
            this.updateGraph();

          })
          .catch((error) =>{
            console.log(error)
          })
    },

    // 编辑节点信息
    Openbox(d)
    {
       this.selectedNode = this.data.nodes[d3.select(d.target).attr("index")];
       this.isVisible = true;
    },
    EditNode(nodeLabel, nodeReference){
      this.selectedNode.label = nodeLabel;
      this.selectedNode.reference = nodeReference;
      this.drawNodeText();
      this.isVisible = false;
    },

    openDrawer(){
      if(this.mouseIsSelect){
        this.isShowDrawer = true;
      }
    },
    closeDrawer(){
      this.isShowDrawer = false;
    },

    // 节点绘制相关
    addNode(source) {
      if(!this.mouseIsSelect) {
        this.data.nodes.push({index: this.data.nodes.length, label: 'Node ' + this.data.nodes.length, reference: '',
          groupId: parseInt(this.$store.state.clickPath[1][2]), x: source.x, y: source.y});
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
              update => update
                  .attr("fill", d => colorList[d.groupId]),
                  // .attr("r", d => d.radius),
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
                  .text(d => {
                    if (d.groupId == 3) {
                      if (d.label.length >= 7) {
                        // return d.label
                        return d.label.substr(0, 4) + '…'
                      }
                      else {
                        return d.label
                      }
                    }
                    else {
                      return d.label
                    }
                  })
                  .call(this.dragger),
              update => update.text(d => {
                if (d.groupId == 3) {
                  if (d.label.length >= 4) {
                    return d.label.substr(0, 4) + '…'
                  }
                  else {
                    return d.label
                  }
                }
                else {
                  return d.label
                }
              }),
              exit => exit.remove()
          );
    },

    // 边绘制相关
    addLink(source, targets) {
      for (const target of targets) {
        this.data.links.push({index: this.data.links.length, source, target});
      }
      this.drawLinks();

      this.simulation.force("link").links(this.data.links);
      this.simulation.alpha(1).restart();
    },
    deleteLink(){
      if(this.mouseIsSelect) {
        this.data.links.splice(this.selectedEdge.index, 1);
        this.drawLinks();
        this.simulation.force("link").links(this.data.links);
        this.simulation.alpha(1).restart();
      }
    },
    drawLinks() {
      this.link = this.link
          .data(this.data.links)
          .join(
              enter => enter.append("path")
                  .attr("fill", "none")
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

      this.link.attr("d", d => this.linkArc(d))

      this.nodeText.attr('transform', d => 'translate(' + d.x + ',' + d.y + ')');

      this.cursor.attr("cx", this.cursorNode.x)
          .attr("cy", this.cursorNode.y);
    },
    linkArc(d){
      if(this.linkNotExist(d.source.index, d.target.index) || this.linkNotExist(d.target.index, d.source.index)) {
        return 'M ' + (d.source.x - offsetX(d)) + ' ' + (d.source.y - offsetY(d))+' L '+ (d.target.x + offsetX(d)) +' '+ (d.target.y + offsetY(d));
      }
      else{
        var dx = d.target.x - d.source.x + 2 * offsetX(d),
            dy = d.target.y - d.source.y + 2 * offsetY(d),
            dr = Math.sqrt(dx*dx+dy*dy) * 1.2;
        return 'M ' + (d.source.x - offsetX(d)) + ' ' + (d.source.y - offsetY(d)) + 'A' + dr + ',' + dr + ' 0 0,1 ' + (d.target.x + offsetX(d)) + ',' + (d.target.y + offsetY(d));
      }

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
          // self.simulation.force("charge", d3.forceManyBody().strength(-100))
          //     .force("link", d3.forceLink(self.data.links).distance(200))
          self.simulation.force("charge", null)
              .force("link", null)
              .force("x", null)
              .force("y", null);
          self.cursor.attr("cx", event.subject.x)
              .attr("cy", event.subject.y);
        }
      }

      function dragged(event) {
        // console.log(event);
        event.subject.fx = event.x;
        event.subject.fy = event.y;

        if (self.$store.state.clickPath && self.$store.state.clickPath[0] === "1"){
          targetNodes = self.data.nodes.filter(node => inRange({x: event.x, y: event.y}, node)).filter(node => self.linkNotExist(event.subject.index, node.index))
          self.mouseLink = self.mouseLink
              .attr("stroke", "#44cef6")
              .attr("stroke-width", 3)
              .attr("stroke-dasharray", 5, 10)
              .data(targetNodes)
              .join("line")
              .attr("x1", event.x)
              .attr("y1", event.y)
              .attr("x2", d => d.x)
              .attr("y2", d => d.y);
          self.cursor.attr("cx", event.x)
              .attr("cy", event.y);
        }
      }

      function dragEnded(event) {
        if (!event.active) self.simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;

        if (self.$store.state.clickPath && self.$store.state.clickPath[0] === "1"){
          self.simulation.force("charge", d3.forceManyBody().strength(-2000))
              .force("link", d3.forceLink(self.data.links).distance(radius * 5))
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

      return d3.drag()
          .on("start", dragStarted)
          .on("drag", dragged)
          .on("end", dragEnded);
    },

    linkNotExist(source, target){
    // console.log(source, target);
    let notExist = true;
    for(let i = 0, len=this.data.links.length; i < len; i++) {
      if(this.data.links[i].source.index === source && this.data.links[i].target.index === target){
        notExist = false;
      }
    }
    return notExist;
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
    width: 75%;
  }
  .text {
    font-size: 15px;
  }
  .item {
    padding: 10px 0;
  }
  /*.box-card {*/
  /*  width: 480px;*/
  /*}*/
</style>