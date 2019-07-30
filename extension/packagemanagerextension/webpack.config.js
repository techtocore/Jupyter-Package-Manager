var path = require('path');

module.exports = {
    entry: './nbextension/extension.js',
    output: {
        path: path.resolve(__dirname, 'packagemanagerextension/nbextension'),
        filename: 'extension.js',
        libraryTarget: 'umd'
    },
    externals: ['jquery', 'base/js/namespace', 'base/js/utils', 'base/js/events', 'require', 'base/js/dialog'],
    module: {
        rules: [{
            test: /\.html$/,
            use: [ {
                loader: 'html-loader',
                options: {
                    minimize: true
                }
            }],
        }]
    }
};
