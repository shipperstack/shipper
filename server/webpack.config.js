const path = require("path");
const webpack = require("webpack");

const buildDate = new Date().toISOString().substring(0, 19);

module.exports = {
  entry: "./frontend/downloads-main.tsx",
  output: {
    filename: "downloads-main.bundle.js",
    path: path.resolve(__dirname, "./downloads/static"),
  },
  module: {
    rules: [
      {
        test: /\.(ts|tsx)$/,
        exclude: /node_modules/,
        loader: "ts-loader",
      },
    ],
  },
  resolve: {
    extensions: [".tsx", ".ts", ".js"],
  },
  plugins: [
    new webpack.DefinePlugin({
      BUILD_DATE: JSON.stringify(buildDate),
    }),
  ],
};
