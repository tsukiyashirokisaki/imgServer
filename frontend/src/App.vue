<template>
  <div id="app">
    <UploadImg/>
    <ViewImg/>
    <Download/>
    <WebSocket/>
    <Markdown/>
  </div>
</template>
<script>
import ViewImg from './components/ViewImg.vue'
import UploadImg from './components/UploadImg.vue'
import Download from './components/Download.vue'
import WebSocket from './components/WebSocket.vue'
import Markdown from './components/Markdown.vue'
import 'github-markdown-css';


export default {
  name: 'App',
  components: {
    UploadImg,
    ViewImg,
    Download,
    WebSocket,
    Markdown
  },
  

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
