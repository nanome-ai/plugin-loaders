module.exports = {
  devServer: {
    proxy: {
      '^/files': {
        target: 'http://localhost',
        ws: true,
        changeOrigin: true
      }
    }
  }
}
