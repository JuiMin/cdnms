const webpack = require('webpack');
const config = {
    entry: __dirname + '/src/index.tsx',
    output: {
        path: __dirname + '/dist',
        filename: 'bundle.js',
    },
    resolve: {
        extensions: ['.js', '.jsx', '.ts', '.tsx', '.css']
    },
    module: {
        rules: [
            {
                test: /\.tsx?/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options:
                    {
                        "presets": [
                            "@babel/preset-env",
                            "@babel/preset-typescript",
                            "@babel/preset-react",
                        ],
                        "plugins": [
                            "@babel/proposal-class-properties",
                            "@babel/proposal-object-rest-spread"
                        ]
                    }
                }
            }
        ]
    },
};
module.exports = config;