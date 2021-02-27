<template>
  <div id="GraphVis" @click="addNode"></div>
</template>

<script>
import vis from 'vis';
export default {
  name: "GraphVis",
  data () {
    return {
      container: null,
      network: null,
      options: null,
      nodes: undefined,
      edges: undefined,
      nodeId: 5,
    }
  },
  mounted(){
    this.create();
  },
  methods: {
    create () {
      // 创建节点组
      this.options = {
        groups: {
          taskNodes: {color:{background:'#FCFE8B'}, borderWidth:1, shape:'circle', title:'任务节点'},
          methodNodes: {color:{background:'#B9F385'}, borderWidth:1, shape:'circle', title:'方法节点'},
          stepNodes: {color:{background:'#75D6C9'}, borderWidth:1, shape:'circle', title:'步骤节点'},
          attributeNodes: {color:{background:'#BC7CDA'}, borderWidth:1, shape:'circle', title:'属性节点'},
          conceptNodes: {color:{background:'#F385A8'}, borderWidth:1, shape:'circle', title:'概念节点'},
        }
      };
      // create an array with nodes
      this.nodes = new vis.DataSet([
        {id: 1, label: 'Node 1', group: 'taskNodes'},
        {id: 2, label: 'Node 2', group: 'methodNodes'},
        {id: 3, label: 'Node 3', group: 'stepNodes'},
        {id: 4, label: 'Node 4', group: 'attributeNodes'},
        {id: 5, label: 'Node 5', group: 'conceptNodes'},
      ]);

      // create an array with edges
      this.edges = new vis.DataSet([
        {from: 1, to: 3},
        {from: 1, to: 2},
        {from: 2, to: 4},
        {from: 2, to: 5},
      ]);

      // 获取容器
      this.container = document.getElementById('GraphVis');

      // 将数据赋值给vis 数据格式化器
      var data = {
        nodes: this.nodes,
        edges: this.edges
      };

      // 初始化关系图
      this.network = new vis.Network(this.container, data, this.options);
    },
    addNode() {
      // 添加节点
      var nodeGroup = '';
      if(this.$store.state.clickPath[0] == "1"){
        switch (this.$store.state.clickPath[1]){
          case "1-1":
            nodeGroup = 'taskNodes';
            break;
          case "1-2":
            nodeGroup = 'methodNodes';
            break;
          case "1-3":
            nodeGroup = 'stepNodes';
            break;
          case "1-4":
            nodeGroup = 'attributeNodes';
            break;
          case "1-5":
            nodeGroup = 'conceptNodes';
            break;
          default:
            nodeGroup = 'undefined';
        }
        this.nodes.add({id: ++this.nodeId, label: 'Node '+this.nodeId, group: nodeGroup})
        console.log(this.nodes);

        // 将数据赋值给vis 数据格式化器
        var data = {
          nodes: this.nodes,
          edges: this.edges
        };

        // 初始化关系图
        this.network = new vis.Network(this.container, data, this.options);
      }
    }
  }
}
</script>

<style>
#GraphVis{
  width: 800px;
  height: 600px;
}
</style>