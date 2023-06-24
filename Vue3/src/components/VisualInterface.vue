<template>
  <div style="padding-top: 20%">
    <h1>
      请在浏览器打开：<a href="http://localhost:7474/browser/" target="_blank"
        >http://localhost:7474/browser/</a>
    </h1>
    <h3>
      该操作需要确认Neo4j驱动已经打开：在命令行中执行“neo4j.bat console”即可
    </h3>
  </div>
</template>

<script>
export default {
  name: "VisualInterface",
  props: {},
  data() {
    return {};
  },
};
</script>

<style scoped>
*{
  font-size: 30px;
  text-align: center;
  line-height: 60px;
  color: #486E53;
}
h3{
 font-size: 20px;
}
</style>