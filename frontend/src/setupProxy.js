const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use('/api/v1', createProxyMiddleware({ target: 'http://0.0.0.0:8000/api/v1/' }))
  app.use('/api/v2', createProxyMiddleware({target: 'http://0.0.0.0:8080/' })
  )
}