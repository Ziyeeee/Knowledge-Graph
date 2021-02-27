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
      // create an array with nodes
      var nodes = new vis.DataSet([
        {id: 1, label: 'Node 1'},
        {id: 2, label: 'Node 2'},
        {id: 3, label: 'Node 3'},
        {id: 4, label: 'Node 4'},
        {id: 5, label: 'Node 5'}
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
      var options = {};

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