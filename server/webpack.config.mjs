// noinspection JSUnusedGlobalSymbols

import path from 'path';
import webpack from 'webpack';

const buildDate = new Date().toISOString().substring(0, 19);

export default {
  entry: './frontend/downloads-main.tsx',
  output: {
    filename: 'downloads-main.bundle.js',
    path: path.resolve(import.meta.dirname, './downloads/static'),
  },
  module: {
    rules: [
      {
        test: /\.(ts|tsx)$/,
        exclude: /node_modules/,
        use: 'ts-loader',
      },
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },
  plugins: [
    new webpack.DefinePlugin({
      BUILD_DATE: JSON.stringify(buildDate),
    }),
  ],
};
