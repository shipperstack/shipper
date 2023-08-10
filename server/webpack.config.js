const path = require('path');

module.exports = {
    entry: './front-end/downloads-main.js',
    output: {
        filename: 'index-bundle.js',
        path: path.resolve(__dirname, './downloads/static'),
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                loader: "babel-loader",
                options: {presets: ["@babel/preset-env", "@babel/preset-react"]}
            },
        ]
    }
}

