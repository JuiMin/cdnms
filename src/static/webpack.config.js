const webpack = require('webpack');
const getConfig = (env) => {
    console.log(env)
    return {
        mode: env && env.NODE_ENV == 'development' ? 'development' : 'production',
        entry: __dirname + '/js/index.jsx',
        output: {
            path: __dirname + '/dist',
            filename: 'bundle.js',
        },
        resolve: {
            extensions: ['.js', '.jsx', '.css']
        },
        module: {
            rules: [
                {
                    test: /\.jsx?/,
                    exclude: /node_modules/,
                    use: {
                        loader: 'babel-loader',
                        options: {
                            "presets": [
                                "@babel/preset-env",
                                "@babel/preset-react"
                            ],
                            "plugins": ["@babel/plugin-proposal-class-properties"]
                        }
                    }
                }
            ]
        },
    }
};
module.exports = getConfig;