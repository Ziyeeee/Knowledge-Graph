module.exports = {
    lintOnSave: false,
    devServer: {
        port: 8080,
        // proxy: {
        //     '/api': {
        //         target: 'http://127.0.0.1:5000/api',
        //         changeOrigin: true,
        //         pathRewrite: {
        //             '^/api': ''
        //         }
        //     }
        // }
    },
};