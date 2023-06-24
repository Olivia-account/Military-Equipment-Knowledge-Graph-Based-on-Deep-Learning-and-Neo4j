<template>
  <div>
    <div id="main">
      <router-view> </router-view>
      <div id="front" v-if="isShow">
        <img src="../../assets/logo.png" alt="" />
        <h1>IME</h1>
        <select name="" id="">
        <option value="">请选择数据集</option>
        <option class="test" v-for="(item, index) in database_info_list" :key="index" :value="item.database_id">
        {{item.name}}
        </option>
          
          
        </select>

        <router-link to="/DataProcessing/Label/LabelPage">
          <button @click="changeisShow" style="margin-left:161px">确 &nbsp;&nbsp;&nbsp; 认</button>
        </router-link>
        <button>自&nbsp; 动 &nbsp;抽&nbsp; 取 </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Label",
 
  props: {},
  data() {
    return {
      isShow: true,
      database_info_list:"",
    };
  },
  methods: {
    changeisShow: function(){
      this.isShow = !this.isShow;
    },
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
  },
  mounted: function () {
    this.databaseList();
   
  },
};
</script>
<style scoped>
#main {
  text-align: center;
}
h1 {
  font-size: 100px;
  color: rgb(107, 146, 77);
  float: left;
  padding: 125px 220px 0px 0px;
}
img {
  float: left;
  padding: 132px 30px 0px 230px;
  height: 100px;
}
button {
  float: left;
  border: none;
  background: rgb(107, 146, 77);
  color: white;
  padding: 8px 20px;
  font-weight: bold;
  border-radius: 15px;
  margin-left: 73px;
  
  width: 190px;
  margin-top: 50px;
}
button:hover {
  cursor: pointer;
}
select {
  float: left;
  margin-left: 160px;
  margin-top: 30px;
  padding: 10px 10px 10px 10px;
  width: 450px;
  border: #ccc solid 1px;
  border-radius: 15px;
  color: #444;
  background: #eee;
}
</style>