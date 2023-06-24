<template>
  <div>
    <div class="right">{{right1}}</div>
  </div>
</template>
<script>
export default {
  props: ["right1"],
}
</script>
<style scoped>
.right {
  float: right;
  padding: 10px;
  background: #017db3;
  margin: 10px 20px 10px 20px;
  color: white;
  border-radius: 5px;
  text-align: right;
  font-size: 16px;
  max-width: 450px;
  clear: both;
}

</style>

