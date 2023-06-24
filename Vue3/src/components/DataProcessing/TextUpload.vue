<template>
<div> 

<!-- <div>暂时不用了</div> -->


  <div id="main" ref="TextUploadMain"> 
  <button @click="move">文 &nbsp; &nbsp; &nbsp;本 &nbsp; &nbsp; &nbsp; 上   &nbsp; &nbsp;&nbsp;传</button></div>
</div>

</template>

<script>
export default {
  name: 'TextUpload',
  props: {

  },
  data() {
    return {

    }
  },
  methods: {
    move(){
      this.$refs.TextUploadMain.style.margin = "100px 0px 0px 0px";
    }
  },
}
</script>
<style scoped>
button{
  border: none;
  background: rgb(107, 146, 77);
  color: white;
  padding: 8px 10px;
  font-weight: bold;
  border-radius: 15px;
  width: 330px;
}
#main {
  margin: 200px 0px 0px 0px;
  width: 100%;
  text-align: center;
}
</style>