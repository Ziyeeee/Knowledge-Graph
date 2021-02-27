<template>
  <div id="GraphVis"></div>
</template>

<script>
import vis from 'vis';
export default {
  name: "GraphVis",
  data () {
    return {
      network: null
    }
  },
  mounted(){
    this.create();
  },
  methods: {
    create () {
      // 创建节点组
      const options = {
        groups: {
          taskNodes: {color:{background:'#FCFE8B'}, borderWidth:1, shape:'circle', title:'任务节点'},
          methodNodes: {color:{background:'#B9F385'}, borderWidth:1, shape:'circle', title:'方法节点'},
          stepNodes: {color:{background:'#75D6C9'}, borderWidth:1, shape:'circle', title:'步骤节点'},
          attributeNodes: {color:{background:'#BC7CDA'}, borderWidth:1, shape:'circle', title:'属性节点'},
          conceptNodes: {color:{background:'#F385A8'}, borderWidth:1, shape:'circle', title:'概念节点'},
        }
      };
      // create an array with nodes
      var nodes = new vis.DataSet([
        {id: 1, label: 'Node 1', group: 'taskNodes'},
        {id: 2, label: 'Node 2', group: 'methodNodes'},
        {id: 3, label: 'Node 3', group: 'stepNodes'},
        {id: 4, label: 'Node 4', group: 'attributeNodes'},
        {id: 5, label: 'Node 5', group: 'conceptNodes'},
        {id: 6, label: 'Node 6'}
      ]);

      // create an array with edges
      var edges = new vis.DataSet([
        {from: 1, to: 3},
        {from: 1, to: 2},
        {from: 2, to: 4},
        {from: 2, to: 5}
      ]);

      // 获取容器
      var container = document.getElementById('GraphVis');

      // 将数据赋值给vis 数据格式化器
      var data = {
        nodes: nodes,
        edges: edges
      };

      // 初始化关系图
      var network = new vis.Network(container, data, options);
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