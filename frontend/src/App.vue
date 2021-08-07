<template>
  <div id="app">
    <UploadImg/>
    <ViewImg/>
  </div>
</template>
<script>
import ViewImg from './components/ViewImg.vue'
import UploadImg from './components/UploadImg.vue'

export default {
  name: 'App',
  components: {
    UploadImg,
    ViewImg
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
