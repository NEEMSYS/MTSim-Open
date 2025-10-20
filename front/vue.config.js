module.exports = {
	devServer: {
		proxy: {
			'/api': {
				target: 'http://114.215.195.207:8000',
				changeOrigin: true,
				pathRewrite: {
					'^/api': '/'
				}
			}
		}
	}
}