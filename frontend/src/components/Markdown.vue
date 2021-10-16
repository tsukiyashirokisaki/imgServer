<template>
    <div class="markdown-body" v-html="htmlMD"></div> 
</template>

<script>
export default {
    name: 'Markdown',
    data() {
        return {
            htmlMD: ''
        };
    },
    mounted() {
        this.htmlMD = require('./keras_ocr_doc.md').default
    },
};
</script>
 <style scoped>
.markdown-body {
   text-align: left;
   margin: 50px;
 }
 </style>