<template>
  <div>
    <div id="main">
      <button>实体检测</button>
      <button>确认融合</button>
      <div class="BiaoGe">
        <table class="xwtable">
          <thead>
            <tr>
              <td>待融合</td>
              <td>已有实体及其相似度</td>
              <td>融合后实体</td>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="(item, index) in newFusionList"
              :key="index"
              :class="{ _dis: !newFusionList[index][3] }"
              @click="discardFusion(index)"
            >
              <td>{{ item[0] }}</td>
              <td>{{ item[1] }}</td>
              <td contenteditable="true">{{ item[2] }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Fusion",
  props: {},
  data() {
    return {
      newFusionList: [
        ["第1条", "内容内容内容", "内容内容内容", true],
        ["第2条", "内容内容内容", "内容内容内容", true],
        ["第3条", "内容内容内容", "内容内容内容", true],
      ],
      id: 1,
    };
  },
  methods: {
    discardFusion: function (index) {
      console.log(this.newFusionList[index]);
      this.newFusionList[index][3] = !this.newFusionList[index][3];
    },
    // 数据融合：加载可融合的node
    loadFusion: function () {
      this.axios
        .post(
          "http://localhost:8000/FindSimilarNode?new_nodes=" +
            JSON.stringify(this.new_nodes)
        )
        .then((res) => {
          if (res.data.length == 0) {
            alert("并未匹配到实体");
          }
          that.new_fusion = [];
          for (item in res.data) {
            for (let i = 0; i < Object.keys(res.data).length; i++) {
              res.data[item]["isChoose"] = "true";
            }
            that.new_fusion.push(res.data[item]);
          }
          console.log("that.new_fusion");
          console.log(that.new_fusion);
        })
        .catch((error) => {
          alert("实体检测失败");
          console.log(error);
        });
    },

    // 数据融合：加载新节点
    loadNodes: function () {
      this.axios
        .get("http://localhost:8000/NewNode?database_id=" + this.id)
        .then((res) => {
          if (res.data == "数据为空") {
            alert("数据集为空");
          }
          console.log("NewNode:");
          console.log(res.data);

        })
        .catch((error) => {
          alert("NewNode failed！");
        });
    },

    // 数据融合：加载新关系
    loadRels: function () {
      this.axios
        .get("http://localhost:8000/NewRel?database_id=" + this.id)
        .then((res) => {
          for (item in res.data) {
            for (let i = 0; i < Object.keys(res.data[item]).length; i++) {
              res.data[item]["rel" + (i + 1)]["isChoose"] = "true";
              that.new_rels.push(res.data[item]["rel" + (i + 1)]);
            }
          }
        })
        .catch((error) => {
          alert("NewRel failed！");
        });
    },
  },
  mounted() {
    this.id = this.$route.params.id;
    // loadFusion();
    // this.loadNodes();
  },
};
</script>
<style scoped>
#main {
  padding-top: 50px;
  text-align: center;
  margin-left: 60px;
}
._dis {
  background: #bbb;
}
button {
  float: left;
  border: none;
  background: rgb(107, 146, 77);
  color: white;
  padding: 8px 10px;
  font-weight: bold;
  border-radius: 15px;
  margin-left: 120px;
  width: 190px;
}
.BiaoGe {
  height: 380px;
  width: 93%;
  /* border: #ccc solid 1px; */
  float: left;
  margin-top: 30px;
  overflow: scroll;
}
.xwtable {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid rgba(107, 147, 77, 0.1);
}

.xwtable thead td {
  color: #486e53;
  text-align: center;
  border: 1px solid rgba(107, 147, 77, 0.1);
  font-weight: bold;
  padding: 10px;
  background: rgba(107, 147, 77, 0.3);
}

.xwtable-tbody {
  overflow: scroll;
  height: 100px;
}

.xwtable tbody tr {
  background: #fff;

  color: #666666;
}
.xwtable tbody tr td {
  text-align: center;
  color: #666666;
}
.xwtable tbody tr.alt-row {
  background: #f2f7fc;
}
.xwtable td {
  line-height: 20px;
  text-align: left;
  padding: 4px 10px 3px 10px;
  height: 18px;
  border: 1px solid rgba(107, 147, 77, 0.1);
}

table tr:nth-child(odd) {
  background: #fff;
}
table tr:nth-child(even) {
  background: #f5faf6;
}
</style>