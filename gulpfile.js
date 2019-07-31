var gulp = require('gulp');
    sass        = require('gulp-sass');
    browserSync = require('browser-sync');
    autoprefixer = require('gulp-autoprefixer')
gulp.task('sass', function(){
    return gulp.src('static/sass/**/*.sass')
        .pipe(sass())
        .pipe(autoprefixer({
            browsers: ['last 4 versions']
        }))
        .pipe(gulp.dest('static/css'))
        .pipe(browserSync.reload({stream: true}))
});

gulp.task('browser-sync', function() {
    browserSync({
        browser: 'chrome',
        server: {
            baseDir: 'static'
        },
        notify: false
    });
});

gulp.task('scripts', function() {
    return gulp.src(['static/js/main.js', 'static/libs/**/*.js'])
    .pipe(browserSync.reload({ stream: true }))
});

gulp.task('code', function() {
    return gulp.src('static/*.html')
    .pipe(browserSync.reload({ stream: true }))
});

gulp.task('watch', function() {
    gulp.watch('static/sass/**/*.sass', gulp.parallel('sass'));
    gulp.watch('html/*.html', gulp.parallel('code'));
    gulp.watch(['static/js/main.js', 'html/libs/**/*.js'], gulp.parallel('scripts'));
});

gulp.task('default', gulp.parallel('sass', 'browser-sync', 'watch'));

