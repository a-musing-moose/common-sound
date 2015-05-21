var gulp = require('gulp');
var config = require('../config');

gulp.task('watch', ['setWatch', 'build'], function() {
    gulp.watch(config.less.watch, ['less']);
    gulp.watch(config.markup.src, ['markup']);
});
