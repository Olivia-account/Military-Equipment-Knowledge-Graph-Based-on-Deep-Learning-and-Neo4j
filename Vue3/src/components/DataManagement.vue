<template>
  <!-- 创建数据集 -->
  <div class="main">
    <!-- 按钮 -->
    <button class="but" @click="showPopup()">
      <a href="javascript:void(0)" style="color: white">创建数据集</a>
    </button>
    <!-- 弹出框 -->
    <div id="overlay">
      <!-- 登录界面 -->
      <div
        style="
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          margin: auto;
          width: 30%;
          height: 81%;
          float: left;
        "
      >
        <!-- 登录模块 -->
        <div
          style="
            width: 100%;
            height: 600px;
            background-color: white;
            float: right;
            border-radius: 5px;
          "
        >
          <a
            href="javascript:void(0)"
            style="
              top: 0px;
              left: 0px;
              float: right;
              margin-right: 10px;
              margin-top: 10px;
            "
            @click="hidePopup()"
            ><img src="../assets/close.png" alt="close" style="width: 15px"
          /></a>
          <div style="width: 100%; height: 10%; float: left; margin-top: 7%">
            <img
              src="../assets/logo.png"
              alt="man"
              style="
                float: left;
                width: 50px;
                margin-left: 34%;
                margin-right: 8px;
              "
            />
            <strong style="float: left; font-size: 40px; color: #609244"
              >IME</strong
            >
          </div>
          <div style="width: 100%; height: 25%"></div>
          <input
            v-model="datasetName"
            type="text"
            placeholder="请输入数据集名称"
            style="
              border: none;
              border-bottom: 1px solid #ddd;

              width: 70%;
              height: 30px;
              text-align: center;
              margin-left: 65px;
              font-size: 17px;
            "
          />

          <textarea
            v-model="remarks"
            cols="30"
            rows="8"
            style="
              resize: none;

              margin-left: 60px;
              margin-top: 45px;
              font-size: 17px;
              padding: 10px;
              border: solid #ddd;
              border-radius: 5px;
            "
            placeholder="备注"
          ></textarea>
          <button
            class="b"
            @click="createDatabases(), hidePopup()"
            style="
              width: 70%;
              height: 40px;
              background-color: #609244;
              color: white;
              border-radius: 10px;
              border: none;
              margin-left: 65px;
              font-size: 20px;
              margin-top: 50px;
            "
          >
            创&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;建
          </button>
        </div>
      </div>
    </div>

    <!-- 测试1 -->
    <div class="test" v-for="(item, index) in database_info_list" :key="index">
      <!-- 第一行 -->
      <div style="float: left; width: 100%; height: 50px">
        <p style="float: left; margin-left: 10px; padding: 14px">
          {{ item.name }}&nbsp;&nbsp;&nbsp;&nbsp;{{ item.create_date }}
        </p>
        <button
          class="del"
          @click="deleteDatabase(e, item.database_id)"
          style="
            float: right;
            margin: 14px;
            margin-right: 40px;
            border: none;
            background-color: white;
            font-size: 16px;
          "
        >
          <img
            src="../assets/bin.png"
            alt="bin"
            style="float: left; width: 23px"
          />
          删除
        </button>
      </div>
      <!-- 第二行 -->
      <div
        style="
          background-color: rgb(247, 247, 247);
          float: left;
          width: 100%;
          height: 50px;
        "
      >
        <div style="width: 15%; height: 100%; float: left; margin-left: 10px">
          <p style="line-height: 50px; padding-left: 15px">ID</p>
        </div>
        <div style="width: 15%; height: 100%; float: left">
          <p style="line-height: 50px; padding-left: 15px">标注类型</p>
        </div>
        <div style="width: 20%; height: 100%; float: left">
          <p style="line-height: 50px; padding-left: 15px">导入状态</p>
        </div>
        <div style="width: 49%; height: 100%; float: left">
          <p style="line-height: 50px; padding-left: 15px">操作</p>
        </div>
      </div>
      <!-- 第三行 -->
      <div
        style="background-color: white; float: left; width: 100%; height: 50px"
      >
        <div style="width: 15%; height: 100%; float: left; margin-left: 10px">
          <p style="line-height: 50px; padding-left: 15px">
            {{ item.database_id }}
          </p>
        </div>
        <div style="width: 15%; height: 100%; float: left">
          <p style="line-height: 50px; padding-left: 15px">
            {{ item.datatype }}
          </p>
        </div>
        <div style="width: 20%; height: 100%; float: left">
          <p style="line-height: 50px; padding-left: 15px">
            {{ item.input_state }}
          </p>
        </div>
        <div style="width: 49%; height: 100%; float: left">
          <p>
            <input
              class="upload"
              name="file"
              type="file"
              accept=".json"
              @change="uploadFiles($event, item.database_id)"
            />
          </p>
          <!-- <button
            style="
              font-size: 17px;
              margin-top: 12px;
              color: black;

              margin-left: 15px;
            "
          >
            Choose File
          </button> -->
          <div class="biaoqian">
            <router-link to="/DataProcessing/Fusion">数据融合</router-link>
          </div>
          <div class="biaoqian">
            <a href="/#/DataProcessing/Label">自动抽取</a>
          </div>
          <div class="biaoqian" @click="dataExport()" style="cursor:pointer;color: #486e53;">导出</div>
        </div>
      </div>
    </div>

    <div style="height: 40px; width: 100%; float: left"></div>
  </div>
</template>

<script>
export default {
  name: "DataManagement",
  props: {},
  data() {
    return {
      datasetName: "",
      remarks: "",
      database_info_list: [],
    };
  },
  methods: {
    showPopup: function () {
      var overlay = document.getElementById("overlay");
      overlay.style.display = "block";
    },
    hidePopup: function () {
      var overlay = document.getElementById("overlay");
      overlay.style.display = "none";
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

    // 数据上传：创建数据集
    createDatabases: function () {
      this.axios
        .get(
          "http://localhost:8000/CreateDatabase?name=" +
            this.datasetName +
            "&remarks=" +
            this.remarks +
            "&datatype=json"
        )
        .then((res) => {
          console.log(res.data);
          // that.msg = res.data.msg;
          // alert(res.data.msg);
          this.datasetName = "";
          this.remarks = "";
          this.databaseList();
          // window.location.reload(true);
        })
        .catch((error) => {
          alert("createDatabases失败");
        });
    },
    // 数据上传：删除数据集
    deleteDatabase: function (e, id) {
      console.log(id);
      this.axios
        .get("http://localhost:8000/DeleteDatabase?database_id=" + id)
        .then((res) => {
          this.databaseList();
        })
        .catch((error) => {
          alert("deleteDatabase失败");
        });
    },
    // 上传数据文件
    uploadFiles: function (e, id) {
      let file = e.target.files[0];
      let param = new FormData(); //创建form对象

      param.append("files", file); //通过append向form对象添加数据
      console.log(param.get("files")); //FormData私有类对象，访问不到，可以通过get判断值是否传进去
      let config = {
        headers: { "Content-Type": "multipart/form-data" }, //这里是重点，需要和后台沟通好请求头，Content-Type不一定是这个值
      }; //添加请求头
      this.axios
        .post("http://localhost:8000/UploadFiles/" + id, param, config)
        .then((res) => {
          alert(res.data.msg);
        })
        .catch((error) => {
          console.log(error);
          alert("deleteDatabase失败");
        });
      alert("文件已上传");
    },
    // 下载数据集压缩包
    dataExport: function () {
      var that = this;
      axios
        .get("http://localhost:8000/DataExport?database_id=" + id)

        .then((res) => {
          alert("请复制以下链接到浏览器中进行下载：" + that.download_url);
        })
        .catch((error) => {
          console.log(error);
          alert("DataExort failed！");
        });
    },
  },

  mounted: function () {
    this.databaseList();
  },
};
</script>

<style scoped>
*{
  color: #555;
}
.main {
  width: 70%;
  align-items: center;
  margin: auto;
  padding-top: 7%;
}

.del:hover {
  cursor: pointer;
}

.upload {
  float: left;
  font-size: 17px;
  margin-top: 12px;
  color: black;
  width: 110px;
  margin-left: 15px;
}

.b:hover {
  cursor: pointer;
}

.but {
  background-color: rgb(107, 146, 77);
  border: none;
  height: 35px;
  width: 100px;
  padding: 5px;
  color: white;
  float: right;
  margin-bottom: 10px;
  border-radius: 5px;
  box-shadow: rgb(0 0 0 / 20%) 0px 3px 10px;
}

.biaoqian {
  height: 100%;
  float: right;
  margin-right: 60px;
  line-height: 50px;
}

a {
  text-decoration: none;
  color: #486e53;
}

.test {
  background-color: white;
  width: 100%;
  float: left;
  margin-top: 20px;
  margin-bottom: 20px;
  border-radius: 5px;
  box-shadow: rgb(0 0 0 / 20%) 0px 3px 10px;
}

#overlay {
  position: fixed;
  left: 0px;
  top: 0px;
  width: 100%;
  height: 100%;
  font-size: 16px;
  background-color: rgba(0, 0, 0, 0.5);
  filter: progid:DXImageTransform.Microsoft.gradient(startColorstr=#7f000000,endColorstr=#7f000000);
  display: none;
}
</style>