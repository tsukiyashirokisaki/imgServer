import Vue from 'vue'
import App from './App.vue'
import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'

const options = { path: '' }; //Options object to pass into SocketIO

Vue.use(new VueSocketIO({
    debug: true,
    connection: SocketIO('http://localhost:5000', options), //options object is Optional
    vuex: {
      actionPrefix: "SOCKET_",
      mutationPrefix: "SOCKET_"
    }
  })
);

Vue.config.productionTip = false


new Vue({
  render: h => h(App),
}).$mount('#app')
