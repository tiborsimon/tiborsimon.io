var gulp = require('gulp');
var concat = require('gulp-concat');
var concatCss = require('gulp-concat-css');
var cssmin = require('gulp-cssmin');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');
 

gulp.task('js', function() {
  return gulp.src([
'themes/rhythm/static/js/jquery-1.11.2.min.js',
'themes/rhythm/static/js/jquery.easing.1.3.js',
'themes/rhythm/static/js/bootstrap.min.js',
'themes/rhythm/static/js/SmoothScroll.js',
'themes/rhythm/static/js/jquery.scrollTo.min.js',
'themes/rhythm/static/js/jquery.localScroll.min.js',
'themes/rhythm/static/js/jquery.viewport.mini.js',
'themes/rhythm/static/js/jquery.countTo.js',
'themes/rhythm/static/js/jquery.appear.js',
'themes/rhythm/static/js/jquery.sticky.js',
'themes/rhythm/static/js/jquery.parallax-1.1.3.js',
'themes/rhythm/static/js/jquery.fitvids.js',
'themes/rhythm/static/js/owl.carousel.min.js',
'themes/rhythm/static/js/isotope.pkgd.min.js',
'themes/rhythm/static/js/imagesloaded.pkgd.min.js',
'themes/rhythm/static/js/jquery.magnific-popup.min.js',
'themes/rhythm/static/js/gmap3.min.js',
'themes/rhythm/static/js/wow.min.js',
'themes/rhythm/static/js/masonry.pkgd.min.js',
'themes/rhythm/static/js/jquery.simple-text-rotator.min.js',
'themes/rhythm/static/js/all.js',
'themes/rhythm/static/js/contact-form.js',
'themes/rhythm/static/js/jquery.ajaxchimp.min.js',
'themes/rhythm/static/js/rrssb.js',
'themes/rhythm/static/js/lightbox.min.js'
])
    .pipe(concat('bundle.js'))
    .pipe(gulp.dest('output/resources/js/'));
});

gulp.task('js-min', function() {
  return gulp.src('output/resources/js/bundle.js')
    .pipe(uglify())
    .pipe(rename({suffix: '.min'}))
    .pipe(gulp.dest('output/resources/js/'));
});

gulp.task('css', function () {
  return gulp.src('themes/rhythm/static/css/*.css')
    .pipe(concatCss("bundle.css"))
    .pipe(gulp.dest('output/resources/css/'));
});
 
gulp.task('css-min', function () {
	gulp.src('output/resources/css/bundle.css')
		.pipe(cssmin())
		.pipe(rename({suffix: '.min'}))
		.pipe(gulp.dest('output/resources/css/'));
});

