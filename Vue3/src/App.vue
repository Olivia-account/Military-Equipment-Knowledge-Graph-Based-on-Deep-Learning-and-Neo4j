<template>
  <div>
    <router-link to="/"></router-link>
    <!-- 顶部导航栏 -->
    <div id="header">
      <!-- Logo -->
      <div class="logo">
        <img src="./assets/logo.png" alt="logo" />
        <h1>IME</h1>
      </div>

      <!-- Tab -->
      <div class="tab_all">
        <router-link
          to="/DataManagement"
          active-class="_active"
          class="tab"
          style="margin-left: 20px"
          >数据管理</router-link
        >
        <router-link to="/DataProcessing" active-class="_active" class="tab"
          >数据处理</router-link
        >
        <router-link to="/Crawl" active-class="_active" class="tab"
          >数据爬虫</router-link
        >
        <router-link to="/Query" active-class="_active" class="tab"
          >知识问答</router-link
        >
        <router-link to="/News" active-class="_active" class="tab"
          >新闻热点</router-link
        >
        <router-link to="/Search" active-class="_active" class="tab"
          >词条检索</router-link
        >
        <router-link to="/VisualInterface" active-class="_active" class="tab"
          >图谱展示</router-link
        >
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "App",
  components: {},
  methods: {},
};
</script>
<style>
::-webkit-scrollbar {
  width: 5px;
  height: 0px;
}
::-webkit-scrollbar-track-piece {
  background-color: transparent;
  -webkit-border-radius: 6px;
}
::-webkit-scrollbar-thumb:vertical {
  height: 12px;
  background-color: #bdbdbd;
  -webkit-border-radius: 6px;
}
::-webkit-scrollbar-thumb:horizontal {
  width: 12px;
  background-color: #bdbdbd;
  -webkit-border-radius: 6px;
}

::-webkit-scrollbar-thumb:vertical:hover,
::-webkit-scrollbar-thumb:horizontal:hover {
  background-color: #808080;
}
</style>