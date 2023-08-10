const path = require('path');

module.exports = {
    entry: './frontend/downloads-main.js',
    output: {
        filename: 'downloads-main.bundle.js',
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

