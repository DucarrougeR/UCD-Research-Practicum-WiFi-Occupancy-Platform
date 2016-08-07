//jshint strict: false
module.exports = function(config) {
    config.set({

        basePath: './app',

        files: [
            'bower_components/angular/angular.js',
            'bower_components/angular-route/angular-route.js',
            'bower_components/angular-mocks/angular-mocks.js',
            'occupancy.js',
            "services/Authentication.js",
            "services/Session.js",
            "services/Permissions.js",
            "services/DataManagement.js",
            "config.js",
            "services/chartData.js",
            "../node_modules/chart.js/dist/Chart.min.js",
            "../node_modules/angular-chart.js/dist/angular-chart.min.js'",
            "../node_modules/pikaday/pikaday.js",
            "../node_modules/pikaday-angular/pikaday-angular.js",
            "../node_modules/ng-file-upload/dist/ng-file-upload.js",
            '**/*.module.js',
            '*!(.module|.spec).js',
            '!(bower_components)/**/*!(.module|.spec).js',
            '**/*.spec.js',
            'components/**/*.js',
            'view*/**/*.js'
        ],

        autoWatch: true,

        frameworks: ['jasmine'],

        browsers: ['Firefox'],


        plugins: [
            'karma-chrome-launcher',
            'karma-firefox-launcher',
            'karma-jasmine',
            'karma-junit-reporter'
        ],

        junitReporter: {
            outputFile: 'test_out/unit.xml',
            suite: 'unit'
        }
    });
};
