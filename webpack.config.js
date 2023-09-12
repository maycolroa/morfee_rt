const path = require("path");
const VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = {
    // mode: 'development',
    mode: 'production',
    entry: "./src_vue/index.js",
    output: {
        filename: 'app.js',
        path: path.resolve(__dirname, "static"),
    },
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.js'
        },
    },
    module: {
        rules: [
            {test: /\.vue$/, use: 'vue-loader'},
            {test: /\.css$/i, use: ['style-loader', 'css-loader']}
        ]
    },
    plugins: [
        new VueLoaderPlugin()
    ]
}