<template>
  <div id="main">
    <textarea
   
      placeholder="请输入需要爬取的网址，若有多个，请用英文逗号隔开"
      v-model="newsList"
    />
    <button @click="AutoCrawl()">自 动 抓 取</button>
    <div id="Beizhu">
      <p> <b> 本功能支持自动爬取的网站为以下几个：</b></p>

      <ul>
        <li>
          <a href="http://www.news.cn/milpro/" target="_blank"> <b>新华军事网</b> </a>
        </li>
        <li>
          <a href="http://mil.cankaoxiaoxi.com/" target="_blank"> <b>参考消息网</b></a>
        </li>
        <li>
          <a href="https://mil.huanqiu.com/" target="_blank"> <b>军事环球网</b></a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "Crawl",
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
  padding-top:15%;

  margin: auto;
  width: 60%;
  text-align: center;
}
ul {
  margin: auto;
 
  margin-top: 10px;
}
li {
  list-style: none;
  
  float: left;
  padding: 13px;
}
textarea {
  float: left;
  resize: none;
  outline: none;
  margin-left: 175px;
  border: #ccc solid 1px;
  padding: 10px;
  width: 55%;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 10px;
  height: 200px;
  font-size: 16px;
  padding-left: 17px;
}
button {
  float: left;
  border: none;
  background: rgb(107, 146, 77);
  color: white;
  padding: 8px 10px;
  font-weight: bold;
  border-radius: 15px;
  margin: 181px -23px 0px 15px;
 
  width: 130px;
  cursor: pointer;
}

#Beizhu {
  margin-top: 110px;
  float: left;
  margin-left: 290px;
}
</style>