var webpack = require("webpack");

module.exports = {
  entry: "./output/theme/js/entry.js",
  output: {
    path: __dirname,
    filename: "output/theme/js/bundle.min.js"
  },
  plugins: [
    new webpack.ProvidePlugin({
      $: "./jquery",
      jQuery: "./jquery"
    }),
    new webpack.ProvidePlugin({
      skel: "./skel"
    }),
    new webpack.optimize.UglifyJsPlugin({minimize: true})
  ]
};
