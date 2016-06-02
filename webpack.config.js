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
      isotope: "./isotope"
    }),
    // new webpack.optimize.UglifyJsPlugin({minimize: true})
  ]
};
