module.exports = {
  devServer: {
    proxy: {
      '^/files': {
        target: 'http://localhost:8081',
        ws: true,
        changeOrigin: true
      }
    }
  }
}
