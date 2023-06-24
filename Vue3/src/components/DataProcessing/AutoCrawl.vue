<template>
  <div id="main">
    <input
      type="text"
      placeholder="请输入需要爬取的网址，若有多个，请用英文逗号隔开"
      v-model="newsList"
    />
    <button @click="AutoCrawl()">自 动 抓 取</button>
    <div id="Beizhu">
      <p>本功能支持自动爬取的网站为以下几个：</p>

      <ul>
        <li>
          <a href="http://www.news.cn/milpro/" target="_blank">新华军事网</a>
        </li>
        <li>
          <a href="http://mil.cankaoxiaoxi.com/" target="_blank">参考消息网</a>
        </li>
        <li>
          <a href="https://mil.huanqiu.com/" target="_blank">军事环球网</a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "AutoCrawl",
  props: {},
  data() {
    return {
      newsList: "",
      
    };
  },
  methods: {
    AutoCrawl: function () {
      this.axios
        .get("http://localhost:8000/NewsCrawl?newsList=" + this.newsList)
        .then((res) => {
          alert("请复制以下链接到浏览器中进行下载：" + res.data);
          this.newsList = "";
        })
        .catch((error) => {
          alert("NewsCrawl failed！");
        });
    },
    
  },
  
};
</script>
<style scoped>
* {
  color: #666;
}
#main {
  margin-top: 200px;
  width: 100%;
  text-align: center;
}
ul {
  margin: auto;
  margin-left: 222px;
  margin-top: 10px;
}
li {
  list-style: none;

  float: left;
  padding: 13px;
}
input {
  outline: none;
  border: #ccc solid 1px;
  padding: 10px;
  width: 55%;
  background: #eee;
  border-radius: 20px;
  height: 25px;
  font-size: 16px;
  padding-left: 17px;
}
button {
  border: none;
  background: rgb(107, 146, 77);
  color: white;
  padding: 8px 10px;
  font-weight: bold;
  border-radius: 15px;
  margin-left: 15px;
  margin-right: -13px;
  width: 130px;
  cursor: pointer;
}

#Beizhu {
  margin-top: 110px;
}
</style>