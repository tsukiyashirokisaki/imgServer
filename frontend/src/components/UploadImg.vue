<template>
  <div class="hello">
    <input type="file" name="image" @change="onFileSelected" id="upload" multiple> <!-- webkitdirectory mozdirectory (folder) -->
    <button @click="onUpload">Upload</button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'UploadImg',
  
  methods: {
    onFileSelected(event){
      this.selectedFiles = event.target.files
      console.log(this.selectedFiles)
    },
    onUpload(){
      const fd = new FormData()
      for (var i=0;i<this.selectedFiles.length;i++){
        console.log(this.selectedFiles[i])
        fd.append("images[]",this.selectedFiles[i],this.selectedFiles[i].name)
      }
      axios.post("/uploadImg",fd, {headers: {
    'accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.8',
    'Content-Type': `multipart/form-data; boundary=${fd._boundary}`
  }}).then(res =>{
        console.log(res);
        document.getElementById("upload").value = ""
      })
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
