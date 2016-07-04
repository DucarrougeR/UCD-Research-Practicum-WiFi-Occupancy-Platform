//jshint strict: false
module.exports = function(config) {
  config.set({

    basePath: './app',

    files: [
      'bower_components/angular/angular.js',
      'bower_components/angular-route/angular-route.js',
      'bower_components/angular-mocks/angular-mocks.js',
<<<<<<< HEAD
      '**/*.module.js',
      '*!(.module|.spec).js',
      '!(bower_components)/**/*!(.module|.spec).js',
      '**/*.spec.js'
=======
      'components/**/*.js',
      'view*/**/*.js'
>>>>>>> 2bd9720733ff289c7c4be284115af17d674c92e5
    ],

    autoWatch: true,

    frameworks: ['jasmine'],

<<<<<<< HEAD
    browsers: ['Chrome', 'Firefox'],
=======
    browsers: ['Chrome'],
>>>>>>> 2bd9720733ff289c7c4be284115af17d674c92e5

    plugins: [
      'karma-chrome-launcher',
      'karma-firefox-launcher',
<<<<<<< HEAD
      'karma-jasmine'
    ]
=======
      'karma-jasmine',
      'karma-junit-reporter'
    ],

    junitReporter: {
      outputFile: 'test_out/unit.xml',
      suite: 'unit'
    }
>>>>>>> 2bd9720733ff289c7c4be284115af17d674c92e5

  });
};
