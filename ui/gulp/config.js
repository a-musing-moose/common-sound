var dest = './static',
    src = './src',
    mui = './node_modules/material-ui/src';

module.exports = {
    less: {
        src: src + '/less/main.less',
        watch: [
            src + '/less/**',
            mui + '/less/**'
        ],
        dest: dest
    },
    markup: {
        src: src + "/www/**",
        dest: dest
    },
    browserify: {
        // Enable source maps
        debug: true,
        // A separate bundle will be generated for each
        // bundle config in the list below
        bundleConfigs: [{
            entries: src + '/app/app.jsx',
            dest: dest,
            outputName: 'app.js'
        }]
    }
};
