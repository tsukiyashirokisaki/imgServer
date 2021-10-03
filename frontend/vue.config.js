module.exports = {
    devServer: {
      proxy: {
            '/socket.io': {
                target: 'http://localhost:5000',
                ws: true,
                changeOrigin: true,
            }
        },
      proxy: 'http://localhost:5000'
    },
    configureWebpack:{
      module: {
        rules: [{
          test: /\.md$/,
          use: [
              {
                  loader: "html-loader"
              },
              {
                  loader: "markdown-loader",
                  options: {
                      /* your options here */
                  }
              }
          ]
      }]
      }
    }
    
  
  }