<template>
  <div style="padding-top: 3%">
    <!-- 中国军事网 -->
    <div class="web" style="float: left">
      <h1 @click="getNews()">中国军事网</h1>
      <ol>
        <li v-for="(item, index) in news1" :key="index">
          <a :href="item[1]" target="_blank">
            {{ item[0] }}
          </a>
        </li>
      </ol>
    </div>
    <!-- 参考信息网 -->
    <div class="web" style="float: right">
      <h1>中国军网</h1>
      <ol>
        <li v-for="(item, index) in news2" :key="index">
          <a :href="item[1]" target="_blank">
            {{ item[0] }}
          </a>
        </li>
      </ol>
    </div>
    <!-- 央广军事网 -->
    <div class="web" style="float: left; margin-bottom: 4%">
      <h1>央广军事网</h1>
      <ol>
        <li v-for="(item, index) in news3" :key="index">
          <a :href="item[1]" target="_blank">
            {{ item[0] }}
          </a>
        </li>
      </ol>
    </div>
  </div>
</template>

<script>
export default {
  name: "News",
  props: {},
  data() {
    return {
      // news1: [],
      // news2: [],
      // news3: [],
      news1:[
      ['中柬“金龙-2023”联合演习：巩固铁杆友谊  深化军事合作', 'https://www.cnr.cn/js2014/zdgz/20230407/t20230407_526210448.shtml'], 
      ['满屏热浪！直击喷火兵昼夜连贯实兵喷火作业考核', 'https://www.cnr.cn/js2014/zdgz/20230406/t20230406_526209381.shtml'], 
      ['祝贺！我国成功发射双曲线一号固体商业运载火箭', 'https://www.cnr.cn/js2014/zdgz/20230407/t20230407_526210586.shtml'],
       ['中柬“金龙-2023”联演举行联合实兵综合演练', 'https://www.cnr.cn/js2014/zdgz/20230406/t20230406_526209216.shtml'], 
       ['南部战区陆军某旅：跨兵种淬火蓄积胜战底气', 'https://www.cnr.cn/js2014/zdgz/20230403/t20230403_526204808.shtml'], 
       ['优秀！祝贺空军首批“双学籍”女飞', 'https://www.cnr.cn/js2014/zdgz/20230406/t20230406_526209391.shtml'], 
       ['清明时节，部队官兵用这样的方式缅怀英烈', 'https://www.cnr.cn/js2014/zdgz/20230405/t20230405_526207982.shtml'],
        ['您的梦想，今已成真', 'https://www.cnr.cn/js2014/zdgz/20230404/t20230404_526206815.shtml'], 
        ['陆军第80集团军某陆航旅飞行训练超酷 大图！', 'https://www.cnr.cn/js2014/zdgz/20230403/t20230403_526204800.shtml'],
         ['多机组协同、长航时演练，直击火热演训场！', 'https://www.cnr.cn/js2014/zdgz/20230402/t20230402_526203692.shtml']],
         news2:[ ['尼日 利亚军方在清剿行动中打死53名武装分子', 'http://news.china.com.cn/2023-04/07/content_85216122.htm'], ['日本自卫队一直升机失事 机上10人含一名师团长', 'http://news.china.com.cn/2023-04/07/content_85215965.htm'], ['外媒紧盯山东舰首进太平洋 专家：此次演训具有很强针对性', 'http://news.china.com.cn/2023-04/07/content_85216383.htm'], ['日本突发! 一自卫队直升机失踪 “机上有10人”', 'http://news.china.com.cn/2023-04/06/content_85215735.htm'], ['国防部新闻发言人就蔡英文“过境”窜美发表谈话', 'http://news.china.com.cn/2023-04/06/content_85213475.htm'], ['日本大幅增加防卫预算遭在野党和民众反对（国际视点）', 'http://news.china.com.cn/2023-04/06/content_85214607.htm'], ['美媒：美军肥胖人数飞速增加，陆军情况尤其糟糕', 'http://news.china.com.cn/2023-04/04/content_85209997.htm'], ['外媒：伊朗海军发现并驱离美军侦察机', 'http://news.china.com.cn/2023-04/03/content_85208353.htm'], ['俄媒：乌前军官称北约无力为乌军生产所需弹药', 'http://news.china.com.cn/2023-04/03/content_85208350.htm'], ['俄国防部：俄防长赴特别军事行动区联合部队指挥部，向俄士兵发奖章', 'http://news.china.com.cn/2023-04/02/content_85206313.htm']],
         news3:[['美新型无人侦察机“悄悄上阵”', 'http://www.81.cn/bq_208581/16214803.html'], ['无 人机投送：美军前沿补给新方式', 'http://www.81.cn/bq_208581/16209370.html'], ['美国海军接收首艘无人运输舰', 'http://www.81.cn/bq_208581/16209369.html'], ['波 兰拟购千余辆新型步战车', 'http://www.81.cn/bq_208581/16207886.html'], ['德印推动扩大双边合作', 'http://www.81.cn/bq_208581/16206264.html'], ['韩日提高政治军 事互动频率', 'http://www.81.cn/bq_208581/16205459.html'], ['不合格销钉导致美加油机停飞', 'http://www.81.cn/bq_208581/16204864.html'], ['深海无人潜航器：应对 海底威胁的新选择', 'http://www.81.cn/bq_208581/16204718.html'], ['美陆军联合作战呈现新动向', 'http://www.81.cn/bq_208581/16204360.html'], ['英新版北极政策直 指经济利益', 'http://www.81.cn/bq_208581/16203915.html']],
        };
  },
  methods: {
    getNews: function () {
      this.axios
        .get("http://localhost:8000/GetNews")
        .then((res) => {
          this.news1 = res.data[0];
          // console.log(this.news1);
          this.news2 = res.data[1];
          // console.log(this.news1);
          this.news3 = res.data[2];
          // console.log(this.news1);
        })
        .catch((error) => {
          alert("GetNews failed！");
        });
    },
  },
  mounted() {
    this.getNews();
  },
};
</script>

<style scoped>
.web {
  background-color: rgba(140, 174, 129, 0.8);
  color: white;
  padding-left: 70px;
  padding-right: 40px;
  padding-top: 20px;
  width: 55%;
  border-radius: 20px;
  margin: 4% 5% 0% 5%;
  box-shadow: rgb(0 0 0 / 20%) 0px 3px 10px;
}
h1 {
  font-size: 30px;
  font-weight: bolder;
  color: white;

  margin-left: -25px;
  margin-top: 10px;
  margin-right: 40px;
  float: left;
}

.web > ol > li {
  float: left;
  width: 780px;

  color: white;
  line-height: 35px;
}

.web > ol > li:first-child {
  margin-top: 20px;
}

.web > ol > li:last-child {
  margin-bottom: 30px;
}

li:hover {
  font-weight: bold;
}
.web > ol > li > a {
  color: white;
  font-size: 18px;
}
</style>