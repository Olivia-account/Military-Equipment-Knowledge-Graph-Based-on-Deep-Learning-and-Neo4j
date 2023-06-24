<template>
  <div style="padding-top: 8%">
    <!-- 小军智能问答助手 -->
    <div class="main">
      <!-- head -->
      <div class="head">
        <span>小军智能问答助手</span>
       
      </div>
      <!-- 对话框 -->
      <div class="dialogue">
        <!-- 对话展示 -->
        <div class="dialogue1" ref="messageContent">
          <div class="left" style="margin-top: 20px">我是智能问答助手小军</div>
          <div v-for="(item, index) in dialogue" :key="index" :class="item[0]">
            {{ item[1] }}
          </div>
        </div>
        <!-- 对话编辑 -->
        <div class="dialogue2">
          <textarea
            v-model="question"
            style="background: rgb(255 255 255 / 0%)"
          ></textarea>
          <button @click="addRight()">发&nbsp;&nbsp;&nbsp;送</button>
        </div>
      </div>
      <!-- 右边栏 -->
      <div style="height: 490px; width: 29%; float: left">
        <div style="height: 50%">
          <h2>热点问题</h2>
          <ul>
            <li>歼-11的生产国</li>
            <li>歼-11的具体数据</li>
            <li>歼-11被装备在哪里</li>
            <li>歼-11在哪里服役</li>
          </ul>
        </div>
        <div style="height: 50%">
          <h2>相关推荐</h2>
          <ul>
            <li>歼-12</li>
            <li>歼-11双座战斗机</li>
            <li>米格-21</li>
            <li>伊-18战斗机</li>
            <li>K180</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Query",
  props: {},
  data() {
    return {
      question: "",
      dialogue: [
        ["right", "歼-11战斗机的数据"],
        [
          "left",
          "外形尺寸：成员：翼展，全高，机翼面积，空挡，重量载荷，最大起飞重量",
        ],
      ],
      ans:'',
    };
  },

  methods: {
    addRight: function () {
      this.dialogue.push(["right", this.question]);
      this.axios
        .get("http://localhost:8000/Query?question=" + this.question)
        .then((res) => {
          this.ans = res.data;
          this.dialogue.push(["left", this.ans]);
          console.log(this.ans);
        })
        .catch((error) => {
          alert("Query failed！");
        });
      this.question = "";
            // 让滚动条始终在最底部
      this.$nextTick(() => {
        this.$refs.messageContent.scrollTop = this.$refs.messageContent.scrollHeight;
      })
    },
   
  },
 

};
</script>

<style scoped>
.main {
  height: 550px;
  width: 50%;
  background: rgb(255 255 255 / 70%);

  padding-top: 0%;
  border-radius: 5px;
  margin: auto;

  box-shadow: rgb(0 0 0 / 20%) 0px 3px 10px;
}
li {
  list-style: none;
}

.head {
  border-radius: 5px 5px 0px 0px;
  float: left;
  width: 100%;
  border-bottom: #e3e3e3 solid 1px;
}
.head > span {
  float: left;
  font-size: 20px;
  line-height: 60px;
  color: #486e53;
  padding-left: 30px;
  font-weight: bold;
}
.dialogue {
  border-right: #e3e3e3 solid 1px;
  height: 490px;
  float: left;
  width: 70%;
}
.dialogue1 {
  height: 70%;
  float: left;
  width: 100%;
  overflow-y: auto;
}

.dialogue1::-webkit-scrollbar {
  width: 5px;
}

.dialogue1::-webkit-scrollbar-thumb {
  background-color: #ccc;

  border-radius: 5px;
}
.dialogue2 {
  border-top: #e3e3e3 solid 1px;
  height: 30%;
  float: left;
  width: 100%;
}
h2 {
  color: #486e53;

  margin: 15px;
  float: left;
  clear: both;
}
li {
  width: 100%;
  float: left;

  padding-left: 15px;
  padding-bottom: 5px;
  color: #486e53;
}
.dialogue > div > button {
  height: 35px;
  width: 100px;
  background: #eee;
  float: right;
  border: none;
  border-radius: 5px;
  color: #6da97e;
  font-weight: bold;
  margin-right: 20px;
}
.dialogue > div > textarea {
  width: 93%;
  height: 60px;
  border: none;
  resize: none;
  padding: 15px;
  outline: none;
}
.left {
  float: left;
  padding: 10px;
  background: #486e53;
  margin: 10px 20px 10px 20px;
  clear: both;
  color: white;
  border-radius: 5px;

  max-width: 400px;
  font-size: 16px;
}
.right {
  float: right;
  padding: 10px;
  background: #017db3;
  margin: 10px 20px 10px 20px;
  color: white;
  border-radius: 5px;
  text-align: right;
  font-size: 16px;
  max-width: 400px;
  clear: both;
}
</style>