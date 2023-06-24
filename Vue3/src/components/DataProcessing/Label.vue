dataAll[0][index].<template>
  <div>
    <div id="main">
      <textarea
        @mouseup="mouseSelect()"
        class="text"
        
        v-model="dataAll[0][index].text"
      ></textarea>
      <div class="four">
        <div>
          <h1>标签标注</h1>
          <div style="height: 180px; overflow: scroll; margin-top: 10px">
            <ul>
              <li
                @dblclick="addNode(item)"
                v-for="(item, index) in labels"
                :key="index"
              >
                {{ item }}
              </li>
            </ul>
          </div>
        </div>
        <div>
          <h1>属性标注</h1>
          <div style="height: 180px; overflow: scroll; margin-top: 10px">
            <ul>
              <li
                @dblclick="addProperties(item)"
                v-for="(item, index) in properties"
                :key="index"
              >
                {{ item }}
              </li>
            </ul>
          </div>
        </div>
        <div>
          <h1>实体</h1>

          <div style="height: 180px; overflow: scroll; margin-top: 10px">
            <ul class="ShiTi">
              <li v-for="(item, key, index) in dataAll[0][index].nodes" :key="index">
                <p
                  @dblclick="discardNode(index)"
                  @click="getTmpIndex(index)"
                  :class="index == tmpIndex ? 'selected' : ''"
                >
                  {{ item.名称 }}
                </p>
                <p
                  @dblclick="discardPro(index, ikeys)"
                  v-for="(iitem, ikeys, iindex) in item"
                  :key="iindex"
                >
                  <span> {{ ikeys }}：</span>
                  <span>{{ iitem }}</span>
                </p>
              </li>
            </ul>
          </div>
        </div>
        <div>
          <h1 style="margin-bottom: 10px">关系</h1>
          <select v-model="relType">
            <option value="生产研发">生产研发</option>
            <option value="属于">属于</option>
            <option value="产国">产国</option>
          </select>
          <span class="add" @click="addRels()">新增</span>
          <div style="height: 145px; overflow: scroll; margin-top: 10px">
            <ul class="GuanXi">
              <li v-for="(item, key, index) in dataAll[0][index].rels" :key="index">
                <input v-model="item.start" />
                <!-- <p>{{ dataAll[0][index].rels[key].start }}</p> -->
                <!-- <input :value="dataAll[0][index].rels[key].start" /> -->
                <p @dblclick="discardRel(index)">{{ item.rel_name }}</p>
                <!-- <input :value="dataAll[0][index].rels[key]['end']" /> -->
                <input v-model="item.end" />
              </li>
            </ul>
          </div>
        </div>
      </div>
      <img
        @click="goPrev()"
        style="cursor: pointer"
        src="../../assets/left.svg"
      />
      <img
        @click="goNext()"
        style="cursor: pointer"
        src="../../assets/right.svg"
      />
      <button @click="Save()">保&nbsp;&nbsp;&nbsp;&nbsp; 存</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "Label",
  props: {},

  data() {
    return {
      tmpText: "",
      labels: [
        "国家",
        "生产研发厂商",
        "枪械与单兵",
        "坦克装甲车辆",
        "火炮",
        "太空装备",
        "爆炸物",
        "战斗机",
        "攻击机",
        "轰炸机",
        "教练机",
        "预警机",
        "侦察机",
        "电子战机",
        "无人机",
        "运输机",
        "飞艇",
        "试验机",
        "加油机",
        "通用飞机",
        "干线",
        "支线",
        "运输直升机",
        "武装直升机",
        "多用途直升机",
        "航空母舰",
        "战列舰",
        "巡洋舰",
        "驱逐舰",
        "护卫舰",
        "两栖作战舰艇",
        "核潜艇",
        "常规潜艇",
        "水雷战舰艇",
        "导弹艇",
        "巡逻舰/艇",
        "保障辅助舰艇",
        "气垫艇/气垫船",
        "其他",
        "非自动步枪",
        "自动步枪t",
        "冲锋枪",
        "狙击枪",
        "手枪",
        "机枪",
        "霰弹枪",
        "火箭筒",
        "榴弹发射器",
        "附件",
        "刀具",
        "迷彩服",
        "步兵战车",
        "主战坦克",
        "特种坦克",
        "装甲运兵车",
        "装甲侦察车",
        "装甲指挥车",
        "救护车",
        "工程抢修车",
        "布/扫雷车",
        "越野车",
        "其他特种装甲车辆",
        "榴弹炮",
        "加农炮",
        "加农榴弹炮",
        "迫击炮",
        "火箭炮",
        "高射炮",
        "坦克炮",
        "反坦克炮",
        "无后坐炮",
        "装甲车载炮",
        "舰炮",
        "航空炮",
        "自行火炮",
        "弹炮结合系统",
        "反弹道导弹",
        "地地导弹",
        "舰地（潜地）导弹",
        "地空导弹",
        "舰空导弹",
        "空空导弹",
        "空地导弹",
        "潜舰导弹",
        "空舰导弹",
        "岸舰导弹",
        "舰舰导弹",
        "航天机构",
        "运载火箭",
        "航天基地",
        "技术试验卫星",
        "军事卫星",
        "科学卫星",
        "应用卫星",
        "空间探测器",
        "航天飞机",
        "宇宙飞船",
        "地雷",
        "水雷",
        "手榴弹",
        "炸弹",
        "鱼雷",
        "火箭弹",
        "原子弹",
        "氢弹",
        "中子弹",
        "飞行器",
        "舰船舰艇",
      ],
      properties: [
        "国家",
        "研发单位与产商",
        "研发时间",
        "投入使用时间",
        "口径",
        "炮管重量",
        "炮管长度",
        "最大射程",
        "炮口初速",
        "型号",
        "全长",
        "弹重",
        "弹长",
        "最大速度",
        "翼展",
        "制导系",
        "引信",
        "宽度",
        "长度",
        "高度",
        "重量",
        "最大行",
        "乘员",
      ],

      nodes: [],
      rels: [],
      relType: "生产研发",
      id: 1,
      dataAll: [[{'text':'ceshi','nodes':{'node1':{}},'rels':{'rel1':{}}}]],
      index: 0,
      tmpIndex: -1,
      dataText: "",
      dataNodes: {},
      dataRels: {},
    };
  },
  methods: {
    // 数据标注：双击删除属性
    discardPro: function (i, ikey) {
      i = i + 1;

      delete this.dataAll[0][this.index].nodes["node" + i.toString()][ikey];
    },
    // 数据标注：双击删除关系
    discardRel: function (i) {
      i = i + 1;
      console.log(i);
      delete this.dataAll[0][this.index].rels["rel" + i.toString()];
      console.log(this.dataAll[0][this.index].rels);
      var count = 1;
      var tmp = this.dataAll[0][this.index].rels
      this.dataAll[0][this.index].rels = {};
      for (let key in tmp){
        this.dataAll[0][this.index].rels['rel'+count.toString()]=tmp[key];
        count++;
      }
      // if(i == this.dataAll[0][this.index].rels.length){
      //   delete this.dataAll[0][this.index].rels["rel" + i.toString()];
      // } else{
        
      // };
      
      console.log(this.dataAll[0][this.index].rels);
    },
    // 数据标注：双击删除实体
    discardNode: function (i) {
      i = i + 1;

      delete this.dataAll[0][this.index].nodes["node" + i.toString()];
    },
    // 数据标注：双击增加实体
    addNode: function (item) {
      var nodesLength =
        Object.keys(this.dataAll[0][this.index].nodes).length + 1;

      this.dataAll[0][this.index].nodes["node" + nodesLength.toString()] = {
        label: [item],
        名称: this.tmpText,
      };
    },

    // 数据标注：增加关系
    addRels: function () {
      this.rels.push();
      var relsLength = Object.keys(this.dataAll[0][this.index].rels).length + 1;
      console.log(this.index, relsLength, this.relType);
      this.dataAll[0][this.index].rels["rel" + relsLength.toString()] = {
        start: "",
        end: "",
        rel_name: this.relType,
      };
    },

    // 数据标注：双击增加属性
    addProperties: function (item) {
      var i = this.tmpIndex + 1;
      this.dataAll[0][this.index].nodes["node" + i.toString()][item] =
        this.tmpText;

      console.log(
        item,
        this.tmpText,
        this.dataAll[0][this.index].nodes["node" + i.toString()]
      );
    },

    getTmpIndex: function (i) {
      if (this.tmpIndex == i) {
        this.tmpIndex = -1;
      } else if (this.tmpIndex != i) {
        this.tmpIndex = i;
      }
    },

    // 数据标注：点击前翻
    goPrev: function () {
      this.index--;
      if (this.index < 0) {
        this.index = this.dataAll[0].length - 1;
      }
      // this.dataNodes = this.dataAll[0][this.index].nodes;
      // this.dataRels = this.dataAll[0][this.index].rels;
      // this.dataText = this.dataAll[0][this.index].text;
      console.log(this.index);
    },

    // 数据标注：点击后翻
    goNext: function () {
      this.index++;
      if (this.index > this.dataAll[0].length-1) {
        this.index = 0;
      }
      // this.dataNodes = this.dataAll[0][this.index].nodes;
      // this.dataRels = this.dataAll[0][this.index].rels;
      // this.dataText = this.dataAll[0][this.index].text;
      console.log(this.dataAll[0].length);
      console.log(this.index);
      // console.log(this.dataAll)
    },
    mouseSelect: function () {
      this.tmpText = window.getSelection().toString();
      console.log(this.tmpText);
    },
    browse: function () {
      this.axios
        .get("http://localhost:8000/Browse?database_id=" + this.id)
        .then((res) => {
          if (res.data == "数据为空") {
            alert("数据集为空");
          }
          console.log("Label的：", res.data);
          this.dataAll = res.data;
          // this.dataNodes = this.dataAll[0][this.index].nodes;
          // this.dataRels = this.dataAll[0][this.index].rels;
          // this.dataText = this.dataAll[0][this.index].text;
        })
        .catch((error) => {
          console.log(error);
          alert("Browse 失败");
        });
    },
    // 数据处理：数据保存
    Save: function () {
      console.log(this.dataAll);

      var data = JSON.stringify(this.dataAll);
      console.log(data);
      this.axios
        .get(
          "http://localhost:8000/DataSave?dataInput=" +
            data +
            "&database_id=" +
            this.id
        )
        .then((res) => {
          alert(res.data.msg);
        })
        .catch((error) => {
          alert("DataSave failed！");
          console.log(error);
        });
    },
  },
  mounted() {
    console.log(this.dataAll[0][this.index].text);
    this.id = this.$route.params.id;
    this.browse();
  },
};
</script>
<style scoped>
* {
  color: #555;
}
#main {
  text-align: center;
}

select {
  padding-left: 5px;
  width: 90px;
  border: #ddd solid 1px;
  border-radius: 5px;

  background: #eee;
  font-size: 14px;
}

.selected {
  background-color: #ddd;
}

.add {
  font-size: 14px;
  color: #444;
  margin-left: 10px;
  font-size: bold;
}
.add:hover {
  cursor: pointer;
}
textarea {
  color: #444;
  background: #eee;
  resize: none;
}

.text {
  float: left;
  margin: 30px 0px 30px 30px;
  padding: 10px;
  font-size: 16px;
  height: 140px;
  width: 90%;
  border: #ccc solid 1px;
  border-radius: 10px;

  float: left;
}
.four > div {
  float: left;
  margin-left: 29px;
  margin-bottom: 25px;
  border: #ccc solid 1px;
  height: 230px;
  width: 20.4%;
  border-radius: 10px;
}
.four > div > div > ul > li {
  list-style: none;
  cursor: pointer;
  font-size: 14px;
}
.four > div > div > ul > li:hover {
  background: #ddd;
}
.four > div > h1 {
  margin-top: 10px;
}

.ShiTi > li > p {
  color: #486e53;
  font-weight: bold;
  font-size: 14px;
  text-align: left;
  margin-left: 10px;
}
.ShiTi > li > p > span:first-child {
  font-size: 13px;
  font-weight: bold;
}
.ShiTi > li > p > span:nth-child(2) {
  font-size: 13px;
  font-weight: 400;
}

.GuanXi > li {
  border: #ddd solid 1px;
  height: 49px;
  width: 130px;
  margin-left: 10px;
  margin-bottom: 5px;
  border-radius: 3px;
}
.GuanXi > li > p {
  line-height: 18px;
  font-size: 13px;
}

.GuanXi > li > input {
  text-align: center;
  border: none;
  font-size: 13px;
  height: 30%;
  width: 100%;
  font-size: 14px;
  color: #363636;
  background: #eee;
}

.GuanXi > li > p:nth-child(2) {
  color: #486e53;
  font-weight: bold;
}

img {
  float: left;
  height: 40px;
  margin-left: 100px;
  margin-right: 60px;
}
button {
  cursor: pointer;
  float: left;
  border: none;
  background: rgb(107, 146, 77);
  color: white;
  padding: 8px 10px;
  font-weight: bold;
  border-radius: 15px;
  margin-left: 136px;
  width: 190px;
}
</style>