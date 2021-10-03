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
        this.getHtmlMD();
    },
    methods: {
        getHtmlMD() {
            this.htmlMD = require('./classify_doc.md').default
            console.log(require('./classify_doc.md'))
            // this.htmlMD = ""
             //匯入md 我這裡根據不同的型別拿不同md檔案
        }
    }
};
</script>
 <style scoped>
.markdown-body {
   text-align: left;
 }
 </style>