<template>
  <div>
    <!-- <div>暂时不用了</div> -->
    <div id="main">
      <select name="" id="">
        <option value="">请选择文本数据</option>
        <option value="">简介.txt</option>
        <option value="">研发背景.txt</option>
        <option value="">结构特点.txt</option>
      </select>
      <textarea id="select_text">
A-32A型攻击机于1958年中期交付完毕。从那时起，两种"矛”式衍生型——J-32B和S-32C开始批量生产。S-32C原型机编号为32901，由编号为32055的A-32A型攻击机改装而成。1957年3月26曰首飞。机上装有几种可供选择的侦察照相设备，并能携带12枚特种闪光弹。这些装备使S-32C可以在夜晚从不同的高度进行照射侦察。S-32C装备了可用于夜间气象条件的导航和搜索设备，并用PS-432/A海上搜索雷达取代了机炮。S-32C除了重新设计的机头下部外，其它部分与A-32A型攻击机极为相似。S-32C最大起飞重量为12500千克。 
1955年,瑞典皇家空军订购了30架S-32C型侦察机，取代了活塞发动机的萨伯-18A型侦察机。1957年，瑞典皇家空军认为订购的攻击机数量过多，就将15架A-32A的订购合同改为15架S-32C型侦察机。除了曾经在F21联队服役过很短的时间（从1959年起)，S-32C型一直在F11联队服役。1978年11月18日，S-32C进行了最后一次飞行后，退出了瑞典皇家空军的战机队伍。</textarea
      >
      <button style="margin-right: 80px">保 存</button>
      <button style="margin-left: 80px">下 载</button>
    </div>
  </div>
</template>
<script>
// window.addEventListener("mouseup", function (e) {
//   let tmp = window.getSelection().toString();
//   console.log(tmp);
// });
export default {
  name: "Optimization",
  props: {},
  data() {
    return {};
  },
};
</script>
<style scoped>
#main {
  padding-top: 50px;
  text-align: center;
}
select {
  padding: 10px 10px 10px 10px;
  width: 400px;
  border: #ccc solid 1px;
  border-radius: 10px;
  color: #444;
  background: #eee;
}
textarea {
  padding: 10px;
  margin-top: 40px;
  height: 260px;
  width: 550px;
  border: #ccc solid 1px;
  border-radius: 10px;
  color: #444;
  background: #eee;
  resize: none;
}

button {
  border: none;
  background: rgb(107, 146, 77);
  color: white;
  padding: 8px 20px 8px 20px;
  font-weight: bold;
  border-radius: 15px;
  margin-left: 15px;
  margin: 40px;
  width: 200px;
}
</style>