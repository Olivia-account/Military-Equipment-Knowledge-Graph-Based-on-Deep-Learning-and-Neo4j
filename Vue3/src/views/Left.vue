<template>
  <div>
    <div class="left">{{left1}}</div>
  </div>
</template>
<script>
export default {
  props: ["left1"],
}
</script>
<style scoped>
.left {
  float: left;
  padding: 10px;
  background: #486e53;
  margin: 10px 20px 10px 20px;
  clear: both;
  color: white;
  border-radius: 5px;

  max-width: 450px;
  font-size: 16px;
}
</style>