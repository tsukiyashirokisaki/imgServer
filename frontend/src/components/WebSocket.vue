<template>
    <div>
        <h1>Log</h1>
  
        <p v-html="log.replace(/(?:\r\n|\r|\n)/g, '<br />')"></p>
    </div>
</template>

<script>
export default {
  name: 'WebSocket',
  data: () => ({ log: null }),
  sockets:{
    connect: function(){  
      this.$socket.emit('log', "init")
      console.log('socket connected')
    },
    message: function(val){
      console.log('返回:'+val)
    }
  },
  mounted () {
  this.sockets.subscribe('log', (event) => {
    this.log = event.data;
  });
}
  
}
</script>    
 <style scoped>
 p {
   text-align: left;
 }
 </style>