<template>
  <div style="padding-top: 8%; width: 70%; margin: auto">
    <div class="main1" v-if="!isShowMain">
      <div class="top">
        <img class="logo" src="../assets/logo.png" alt="" />
        <h1>IME</h1>
      </div>
      <div class="choose">
        <select name="" id="" v-model="id">
          <option value="">请选择数据集</option>
          <option
            class="test"
            v-for="(item, index) in database_info_list"
            :key="index"
            :value="item.database_id"
          >
            {{ item.name }}
          </option>
        </select>

        <button @click="transfer()">确 &nbsp;&nbsp;&nbsp; 认</button>
      </div>
    </div>
    <div class="main2" v-if="isShowMain">
      <div class="leftBar">
        <div style="margin-top: 40px">关系抽取</div>
        <ul>
          <li>
            <img src="../assets/右箭头.svg" v-if="isShow[0]" /><router-link
              :to="`/DataProcessing/Label/${id}`"
              active-class="_active"
              @click="changeisShow1"
              >数据标注</router-link
            >
          </li>
        </ul>
        <div>图谱更新</div>
        <ul>
          <li>
            <img src="../assets/右箭头.svg" v-if="isShow[1]" /><router-link
              :to="`/DataProcessing/DataUpload/${id}`"
              active-class="_active"
              @click="changeisShow2"
              >数据上传</router-link
            >
          </li>
          <li>
            <img src="../assets/右箭头.svg" v-if="isShow[2]" /><router-link
              :to="`/DataProcessing/Fusion/${id}`"
              active-class="_active"
              @click="changeisShow3"
              >实体融合</router-link
            >
          </li>
        </ul>
      </div>

      <div class="main">
        <router-view> </router-view>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DataProcessing",
  props: {},
  data() {
    return {
      isShowMain: false,
      isShow: [true, false, false],
      database_info_list: [],
      id: "",
      data: [],
      index: 1,
    };
  },
  methods: {
    // 获取数据集列表
    databaseList: function () {
      this.axios
        .get("http://localhost:8000/DatabaseList")
        .then((res) => {
          this.database_info_list = JSON.parse(JSON.stringify(res.data));
          console.log(this.database_info_list);
        })
        .catch((error) => {
          alert("databaseList失败");
        });
    },
    transfer: function () {
      if (this.id != "") {
        this.isShowMain = !this.isShowMain;
        this.browse(this.id);
      } else {
        alert("请选择数据集！");
      }
    },
    // 数据标注：展示数据集的数据
    browse: function (id) {
      this.axios
        .get("http://localhost:8000/Browse?database_id=" + id)
        .then((res) => {
          if (res.data == "数据为空") {
            alert("数据集为空");
          }
          console.log(res.data);
          this.data = res.data;
      
        })
        .catch((error) => {
          alert("Browse 失败");
        });
    },

    changeisShow1: function () {
      this.isShow = [true, false, false]; //取反
    },
    changeisShow2: function () {
      this.isShow = [false, true, false]; //取反
    },
    changeisShow3: function () {
      this.isShow = [false, false, true]; //取反
    },
 
  },
  mounted: function () {
    this.databaseList();
    // this.isShow = this.$route.query.isShow;
  },
};
</script>

<style scoped>
* {
  color: #666;
}
.main1 {
  text-align: center;
  width: 75%;
  margin: auto;
}
.leftBar {
  float: left;
  height: 550px;
  background: rgba(240, 240, 240, 0.6);
  width: 20%;
  border-radius: 15px;
  box-shadow: rgb(0 0 0 / 20%) 0px 3px 10px;
}

.main {
  float: right;
  height: 550px;
  width: 76%;
  background: rgba(240, 240, 240, 0.6);

  border-radius: 15px;
  box-shadow: rgb(0 0 0 / 20%) 0px 3px 10px;
}
li {
  list-style: none;
}
.leftBar > div {
  text-align: center;
  line-height: 60px;
  font-weight: bold;
}
.leftBar > ul > li {
  text-align: center;
  line-height: 40px;
  width: 100%;
}
.leftBar > ul > li:hover {
  color: #486e53;
  border-left: #486e53 5px solid;
}
._active {
  color: #486e53;
  font-weight: bold;
  width: 100%;
}
img {
  height: 20px;
  margin-right: 10px;
  margin-bottom: -5px;
  margin-left: -31px;
}

h1 {
  font-size: 100px;
  color: rgb(107, 146, 77);
  float: left;
  padding: 143px 220px 0px 0px;
}
.logo {
  float: left;
  padding: 142px 30px 0px 230px;
  height: 100px;
}

.top {
  width: 100%;
}
.choose {
  width: 100%;
}
button {
  float: left;
  border: none;
  background: rgb(107, 146, 77);
  color: white;
  padding: 10px 20px;
  font-weight: bold;
  border-radius: 15px;

  width: 150px;
  margin-top: 71px;
  margin-left: 31px;
}
button:hover {
  cursor: pointer;
}
select {
  float: left;

  margin: auto;
  margin-top: 70px;
  margin-left: 125px;
  padding: 10px 10px 10px 10px;
  width: 350px;
  border: #ccc solid 1px;
  border-radius: 15px;
  color: #444;
  background: #eee;
}
</style>