<template>
  <div>
    <div id="main">
      <h1 style="margin-right: 50px">实体</h1>
      <h1>关系</h1>
      <div class="left">
        <div style="height: 100%; overflow: scroll">
          <ul class="ShiTi">
            <li
              :class="{ _dis: !item.Choose }"
              @click="discardNode(index)"
              v-for="(item, index) in newNode"
              :key="index"
            >
              
              <p>{{ item.名称 }}</p>
              <p v-for="(iitem, ikeys, iindex) in item" :key="iindex">
                <span>{{ ikeys }}：</span>
                <span>{{ iitem }}</span>
              </p>
            </li>
          </ul>
        </div>
      </div>
      <div class="right">
        <div style="height: 100%; overflow: scroll">
          <ul class="GuanXi">
            <li
              :class="{ _dis: !item.Choose }"
              @click="discardRel(index)"
              v-for="(item, index) in newRel"
              :key="index"
            >
              <p>{{ item.start }}</p>
              <p>{{ item.rel_name }}</p>
              <p>{{ item.end }}</p>
            </li>
          </ul>
        </div>
      </div>
      <button style="margin-right: 50px">上 传 实 体</button>
      <button>上 传 关 系</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "DataUpload",
  props: {},
  data() {
    return {
      newNode: [],
      newRel: [],
 
      id: 0,
    };
  },
  methods: {
    discardNode: function (index) {

        this.newNode[index].Choose = !this.newNode[index].Choose;
    },
    discardRel: function (index) {
      this.newRel[index].Choose = !this.newRel[index].Choose;
    },
    // 数据融合：加载新节点
    loadItems: function () {
      this.axios
        .get("http://localhost:8000/NewItem?database_id=" + this.id)
        .then((res) => {
          if (res.data == "数据为空") {
            alert("数据集为空");
          }
          this.newNode = res.data[0];
          this.newRel = res.data[1];
          // console.log(res.data);

        })
        .catch((error) => {
          alert("NewNode failed！");
        });
    },
  },
  mounted() {
    this.id = this.$route.params.id;
    this.loadItems();
  },
};
</script>
<style scoped>
* {
  color: #666;
}

#main {
  width: 90%;
  margin-left: 50px;
  padding-top: 40px;
}
#main > div {
  height: 320px;
  border: #ccc solid 1px;
  width: 41%;
  float: left;
  border-radius: 15px;

  padding: 10px 0px 10px 20px;
}
h1 {
  float: left;
  width: 44%;
  text-align: center;
  font-size: 20px;
  margin-bottom: 20px;
  color: #486e53;
}
.left {
  margin-right: 50px;
}
button {
  float: left;
  border: none;
  background: rgb(107, 146, 77);
  color: white;
  padding: 8px 10px;
  font-weight: bold;
  border-radius: 15px;
  margin-top: 30px;
  width: 44.5%;
}
.ShiTi > li {
  width: 250px;
}
._dis {
  background: #bbb;
}
.ShiTi > li > p:first-child {
  font-weight: bold;
  margin-top: 10px;
  color: #486e53;
}
.ShiTi > li > p > span:first-child {
  font-size: 14px;
  font-weight: 400;
  margin-top: 10px;
}
.ShiTi > li > p > span:nth-child(2) {
  font-size: 14px;
}
.GuanXi > li {
  margin-top: 10px;
  width: 250px;
}
.GuanXi > li > p:nth-child(2) {
  color: #486e53;
  font-weight: bold;
}
</style>