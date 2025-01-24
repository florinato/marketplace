const path = require('path');

module.exports = {
  entry: './src/index.js', // Entry point of your React application
  output: {
    path: path.resolve(__dirname, 'dist'), // Output directory for bundled files
    filename: 'bundle.js', // Name of the bundled file
  },
  module: {
    rules: [
      {
        test: /\.js$/, // Apply loader to .js files
        exclude: /node_modules/, // Exclude node_modules directory
        use: {
          loader: 'babel-loader', // Use babel-loader for transpiling
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react']
          }
        }
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.jsx'], // Allow importing .js and .jsx files without specifying extension
  },
  mode: 'development', // Set mode to development for development build
};
