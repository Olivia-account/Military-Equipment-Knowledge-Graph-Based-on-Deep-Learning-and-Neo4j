
<template>
  <div style="padding-top: 5%; width: 70%; margin-left: 205px">
    <!-- 搜索框 -->
    <div class="searchBar">
      <img
        @click="detailSearch()"
        class="img1"
        src="../assets/scope.svg"
        alt="scope"
      />
      <input v-model="query" type="text" placeholder="军事装备搜索" />
      <img class="img2" src="../assets/logo.png" alt="logo" />
    </div>
    <!-- 背景 -->
    <div class="bg">
      <div v-if="Object.keys(query_ans).length <= 0" class="TiXing">
        请输入关键词进行搜索
      </div>
      <div v-if="Object.keys(query_ans).length > 0">
        <h1>{{ query_ans.名称 }}</h1>

        <div style="width: 94%; float: left">
          <p>{{ query_ans.简介 }}</p>
          <img
            :src="`../../static/pic/${query_ans.pic_path}`"
            alt="图片暂无收录"
          />
        </div>
        <div style="width: 94%; float: left">
          <h1 style="margin-top: 40px; font-size: 35px">武器性能</h1>
          <div class="biaoGe">
            <p v-for="(item, key, index) in query_ans2" :key="index">
              <span>{{ key }}：{{ item }}</span>
            </p>

            <div style="height: 60px; width: 100%; float: left"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Search",
  props: {},
  data() {
    return {
      query: "Saab-32“矛”式战机",
      t: "../../static/pic/021型导弹艇.jpg",
      query_is_null: "",
      query_ans: {},
      query_ans2: {},
    };
  },
  methods: {
    
    detailSearch: function () {
      this.axios
        .get("http://localhost:8000/DetailSearch?aim=" + this.query)
        .then((res) => {
          // this.query_is_null = res.data != null;
          this.query_ans = res.data;

          console.log(this.query_ans);

          if (this.query_ans.简介 == "") {
            this.query_ans.简介 = "暂无简介";
          }
        })
        .catch((error) => {
          alert("DetailSearch failed！");
        });
      this.axios
        .get("http://localhost:8000/DetailSearch?aim=" + this.query)
        .then((res) => {
          this.query_ans2 = res.data;
          delete this.query_ans2._id;
          delete this.query_ans2.简介;
          delete this.query_ans2.图片;
          delete this.query_ans2.pic_path;
          console.log(this.query_ans2);
        })
        .catch((error) => {
          alert("DetailSearch failed！");
        });
    },
  },
};
</script>

<style scoped>
* {
  color: white;
  font-size: 20px;
}

.TiXing {
  line-height: 500px;
  text-align: center;
  font-size: 50px;
  margin-left: -50px;
}

.bg {
  width: 100%;
  background-color: #8cae81;
  opacity: 0.8;
  color: white;
  padding-left: 60px;
  padding-top: 50px;
  border-radius: 20px;
  float: left;
  margin: auto;
  margin-top: 40px;
  margin-bottom: 50px;
  box-shadow: rgb(0 0 0 / 20%) 0px 3px 10px;
}
h1 {
  font-size: 40px;
  margin-bottom: 10px;
}

.searchBar {
  float: right;
  margin-top: 30px;
  /*margin-right: 130px;*/
}

.img2 {
  width: 30px;
  float: right;
  margin-right: 15px;
  margin-top: 2px;
}

.img1 {
  width: 20px;
  float: right;
  margin-left: 10px;
  margin-top: 5px;
}

.img1 :hover {
  cursor: pointer;
}

.searchBar > input {
  width: 250px;
  float: right;
  border: 1px #ddd solid;
  padding: 5px 10px 5px 10px;
  border-radius: 10px;
  outline: none;
  font-size: 16px;
  color: #777;
}

.bg > div > div > p {
  margin-top: 30px;
  width: 550px;
  float: left;
  line-height: 30px;
}

.bg > div > div > img {
  margin-top: 30px;
  width: 350px;
  float: right;
}
.biaoGe {
  width: 100%;
  margin-top: 30px;
}
.biaoGe > p {
  float: left;
  border-bottom: #ddd dotted 3px;
  width: 50%;
  line-height: 50px;
}

.biaoGe > p > span {
  width: 100%;
  float: left;
}
</style>