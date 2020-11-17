module.exports = {
    css: {
        loaderOptions: {
            less: {
            javascriptEnabled: true // 解决main.js  引入antd less 样式bug
            }
        }
        },
    devServer: {
        // watchOptions: {
        //     ignored: ['node_modules']
        // },
        // proxy: 'http://172.0.0.9:5000/',
        proxy: {
            '/': {
              target: 'http://172.0.0.9:5000/',
              changeOrigin: true
                },
            },
        public: '127.0.0.1:7080',
        disableHostCheck: true
    },
    
    productionSourceMap: false, // 去除 source map 

    //修改或新增html-webpack-plugin的值，在index.html里面能读取htmlWebpackPlugin.options.title
    chainWebpack: config =>{
        config.plugin('html')
        .tap(args => {
            args[0].title = "数据平台";
            return args;
        })
    },
}