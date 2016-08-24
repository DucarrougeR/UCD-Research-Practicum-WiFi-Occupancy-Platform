var gulp = require('gulp'),
    gp_concat = require('gulp-concat'),
    gp_rename = require('gulp-rename'),
    gp_uglify = require('gulp-uglify'), css_minify = require('gulp-minify-css');

//     <script src="{{ url_for('static', filename='app/bower_components/angular/angular.js') }}"></script>
// <script src="{{ url_for('static', filename='app/bower_components/angular-route/angular-route.js') }}"></script>
// <script src="{{ url_for('static', filename='app/occupancy.js') }}"></script>
// <script src="{{ url_for('static', filename='app/services/Authentication.js') }}"></script>
// <script src="{{ url_for('static', filename='app/services/Session.js') }}"></script>
// <script src="{{ url_for('static', filename='app/services/Permissions.js') }}"></script>
// <script src="{{ url_for('static', filename='app/services/DataManagement.js') }}"></script>
// <script src="{{ url_for('static', filename='app/services/RoomOccupancy.js') }}"></script>
// <script src="{{ url_for('static', filename='app/services/Modules.js') }}"></script>
// <script src="{{ url_for('static', filename='app/directives/loggedInUser.js') }}"></script>
// <script src="{{ url_for('static', filename='app/config.js') }}"></script>

// <script src="{{ url_for('static', filename='node_modules/chart.js/dist/Chart.min.js') }}"></script>
// <script src="{{ url_for('static', filename='node_modules/angular-chart.js/dist/angular-chart.min.js') }}"></script>
// <script src="{{ url_for('static', filename='node_modules/pikaday/pikaday.js') }}"></script>
// <script src="{{ url_for('static', filename='node_modules/pikaday-angular/pikaday-angular.js') }}"></script>
// <script src="{{ url_for('static', filename='node_modules/ng-file-upload/dist/ng-file-upload.js') }}"></script>

gulp.task('angular-concat', function(){
    return gulp.src(['app/bower_components/angular/angular.js', 
    	'app/bower_components/angular-route/angular-route.js', 
    	'node_modules/chart.js/dist/Chart.min.js',
    	'node_modules/angular-chart.js/dist/angular-chart.min.js',
    	'node_modules/pikaday/pikaday.js',
    	'node_modules/pikaday-angular/pikaday-angular.js',
    	'node_modules/ng-file-upload/dist/ng-file-upload.js'])
        .pipe(gp_concat('angular-concat.js'))
        .pipe(gulp.dest('app'))
        .pipe(gp_rename('angular-concat.min.js'))
        .pipe(gp_uglify())
        .pipe(gulp.dest('app'));
});

gulp.task('app-concat', function(){
    return gulp.src(['app/occupancy.js', 
    	'app/services/Authentication.js', 
    	'app/services/Session.js',
    	'app/services/Permissions.js',
    	'app/services/DataManagement.js',
    	'app/services/RoomOccupancy.js',
    	'app/services/Modules.js',
    	'app/config.js'
    	])
        .pipe(gp_concat('app-concat.js'))
        .pipe(gulp.dest('app'))
        .pipe(gp_rename('app-concat.min.js'))
        .pipe(gp_uglify())
        .pipe(gulp.dest('app'));
});

gulp.task('minify-css', function() {
	gulp.src('css/main.css')
   .pipe(css_minify())
   .pipe(gulp.dest('css/main.min.css'));
});

gulp.task('default', ['angular-concat', 'app-concat', 'minify-css'], function(){});