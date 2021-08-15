<template>
  <a
  :href="item.url"
  v-text="item.label"
  @click="downloadItem(item)" 
  />
</template>

<script>
import axios from 'axios'
export default {
  name: 'Download',
  methods: {
  downloadItem ({ url, label }) {
    axios.get(url, { responseType: 'blob' })
      .then(response => {
        console.log(response)
        const blob = new Blob([response.data], { type: 'application/' })
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = label
        link.click()
        URL.revokeObjectURL(link.href)
        
      })
  }
},
    computed: {
        item(){
            console.log("compute")
            return {url:"/file/yolov5s.pt",label:"yolov5s.pt"}
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
} 
a {
  color: #42b983;
}
</style>
