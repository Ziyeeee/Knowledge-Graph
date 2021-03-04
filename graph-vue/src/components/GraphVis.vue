<template>
  <div id="GraphVis" @click="addNodes"></div>
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
      data: undefined,
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
        local: 'cn',
        cn: {
          addDescription: "单击空白处放置新节点。",
          addEdge: "添加连接线",
          addNode: "添加节点",
          back: "返回",
          close: "關閉",
          createEdgeError: "无法将连接线连接到群集。",
          del: "删除选定",
          deleteClusterError: "无法删除群集。",
          edgeDescription: "单击某个节点并将该连接线拖动到另一个节点以连接它们。",
          edit: "编辑",
          editClusterError: "无法编辑群集。",
          editEdge: "编辑连接线",
          editEdgeDescription: "单击控制节点并将它们拖到节点上连接。",
          editNode: "编辑节点"
        },
        groups: {
          taskNodes: {color:{background:'#FCFE8B'}, borderWidth:1, shape:'circle', title:'任务节点'},
          methodNodes: {color:{background:'#B9F385'}, borderWidth:1, shape:'circle', title:'方法节点'},
          stepNodes: {color:{background:'#75D6C9'}, borderWidth:1, shape:'circle', title:'步骤节点'},
          attributeNodes: {color:{background:'#BC7CDA'}, borderWidth:1, shape:'circle', title:'属性节点'},
          conceptNodes: {color:{background:'#F385A8'}, borderWidth:1, shape:'circle', title:'概念节点'},
        },
        manipulation: {
          enabled: true,
          initiallyActive: false,
          addNode: true,
          addEdge: true,
          editNode: undefined,
          editEdge: true,
          deleteNode: true,
          deleteEdge: true,
          controlNodeStyle:{
          }
        }
      };
      // create an array with nodes
      var nodes = new vis.DataSet([
        {id: 1, label: 'Node 1', group: 'taskNodes'},
        {id: 2, label: 'Node 2', group: 'methodNodes'},
        {id: 3, label: 'Node 3', group: 'stepNodes'},
        {id: 4, label: 'Node 4', group: 'attributeNodes'},
        {id: 5, label: 'Node 5', group: 'conceptNodes'},
      ]);
       console.log(nodes)

      // create an array with edges
      var edges = new vis.DataSet([
        {from: 1, to: 3},
        {from: 1, to: 2},
        {from: 2, to: 4},
        {from: 2, to: 5},
      ]);

      // 获取容器
      this.container = document.getElementById('GraphVis');

      // 将数据赋值给vis 数据格式化器
      this.data = {
        nodes:  nodes,
        edges: edges
      };

      // 初始化关系图
      this.network = new vis.Network(this.container, this.data, this.options);
      this.network.enableEditMode()
      this.network.editNode();
    },
    addNodes() {
      // 添加节点
      var nodeGroup = '';
      if(this.$store.state.clickPath[0] == "1"){
        switch (this.$store.state.clickPath[1]){
          case "1-1":
            nodeGroup = 'taskNodes';

            // this.data.nodes.add({id: ++this.nodeId, label: 'Node '+this.nodeId, color:{background:'#FCFE8B'}, borderWidth:1, shape:'circle', title:'任务节点'});
            break;
          case "1-2":
            nodeGroup = 'methodNodes';
            // this.data.nodes.add({id: ++this.nodeId, label: 'Node '+this.nodeId, color:{background:'#B9F385'}, borderWidth:1, shape:'circle', title:'方法节点'});
            break;
          case "1-3":
            nodeGroup = 'stepNodes';
            // this.data.nodes.add({id: ++this.nodeId, label: 'Node '+this.nodeId, color:{background:'#75D6C9'}, borderWidth:1, shape:'circle', title:'步骤节点'});
            break;
          case "1-4":
            nodeGroup = 'attributeNodes';
            // this.data.nodes.add({id: ++this.nodeId, label: 'Node '+this.nodeId, color:{background:'#BC7CDA'}, borderWidth:1, shape:'circle', title:'属性节点'});
            break;
          case "1-5":
            nodeGroup = 'conceptNodes';
            // this.data.nodes.add({id: ++this.nodeId, label: 'Node '+this.nodeId, color:{background:'#F385A8'}, borderWidth:1, shape:'circle', title:'概念节点'});
            break;
          default:
            nodeGroup = 'undefined';
            // this.data.nodes.add({id: ++this.nodeId, label: 'Node '+this.nodeId});
        }

        this.data.nodes.add({id: ++this.nodeId, label: 'Node '+this.nodeId, group: nodeGroup});

        console.log(this.network);
      }
    }
  }
}
</script>

<style>
#GraphVis{
  width: 800px;
  height: 600px;
  margin: 10px;
}
</style>