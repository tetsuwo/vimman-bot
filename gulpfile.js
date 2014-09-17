var gulp    = require('gulp'),
    connect = require('gulp-connect'),
    concat  = require('gulp-concat'),
    uglify  = require('gulp-uglify'),
    jshint  = require('gulp-jshint');

gulp.task('default', function () {
  // place code for your default task here
});

gulp.task('connect', function () {
  connect.server({
    root: './public',
    livereload: true
  });
});

gulp.task('concat', function () {
  var targets = gulp.src([
      'public/assets/js/app/utils.js',
      'public/assets/js/app/helpers.js',
      'public/assets/js/app/components/questions/index.js',
      'public/assets/js/app/components/questions-create/index.js',
      'public/assets/js/app/components/questions-update/index.js',
      'public/assets/js/app/components/operators/index.js',
      'public/assets/js/app/components/operators-create/index.js',
      'public/assets/js/app/components/operators-update/index.js',
      'public/assets/js/app/components/informations/index.js',
      'public/assets/js/app/components/informations-create/index.js',
      'public/assets/js/app/components/informations-update/index.js',
      'public/assets/js/app/components/responses/index.js',
      'public/assets/js/app/components/responses-create/index.js',
      'public/assets/js/app/components/responses-update/index.js',
      'public/assets/js/app/components/tweets/index.js',
      'public/assets/js/app/components/pagination/index.js',
      'public/assets/js/app/app.js',
      'public/assets/js/app/router.js'
    ]);

  targets
    .pipe(concat('project.js'))
    .pipe(jshint())
    .pipe(gulp.dest('public/assets/js'));

  targets
    .pipe(concat('project.min.js'))
    .pipe(jshint())
    .pipe(uglify())
    .pipe(gulp.dest('public/assets/js'));
});

gulp.task('html', function () {
  gulp.src('./public/*.html')
    .pipe(connect.reload());
});

gulp.task('watch', function () {
  gulp.watch(['./public/*.html'], ['html']);
  gulp.watch(['./public/assets/js/**'], ['concat']);
});

gulp.task('default', ['connect', 'watch']);
