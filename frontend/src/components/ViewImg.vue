
<template>
  <div>
  <h1>Train</h1>
  <div v-for="item in trainImgs.imgs" :key="item" class="box">
    <img :src="trainImgs.root+item"/>
    <p>{{item}}</p>
  </div>
  <div class="clear-line"/>
  <h1>Validation</h1>
  <div v-for="item in valImgs.imgs" :key="item" class="box">
    <img :src="valImgs.root+item"/>
    <p>{{item}}</p>
  </div>
  </div>
</template>

<script>
import axios from 'axios'
import Vuex from 'vuex'
import Vue from 'vue'
Vue.use(Vuex)
const store = new Vuex.Store({
  state: {
    trainImgs: [],
    valImgs: []
  },
  mutations: {
    pushTrainImgs (state,imgs) {
      state.trainImgs = imgs
    },
    pushValImgs (state,imgs) {
      state.valImgs = imgs
    }
  }
})

export default {
  name: 'ViewImg',
  store,
  created(){
      axios.get("/addBox")
      .then(response => {
          store.commit("pushTrainImgs",response["data"]["boxList"]["train"])
          store.commit("pushValImgs",response["data"]["boxList"]["val"])})
  },
  computed: {
    trainImgs () {
      return store.state.trainImgs
    },
    valImgs (){
      return store.state.valImgs
    }
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
img {
    height:150px;
    margin:5px;
}
.box {
  display:inline-block;
  margin:0 auto;
}
.clear-line{
  clear:left;
}
</style>
