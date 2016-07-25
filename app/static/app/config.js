'use strict';

angular.
  module('occupancyApp').
  config(['$locationProvider' ,'$routeProvider', '$logProvider', 'ChartJsProvider',
    function config($locationProvider, $routeProvider, $logProvider, ChartJsProvider) {
      console.log("loaded config");
      //$locationProvider.hashPrefix('!');
      $logProvider.debugEnabled(true);

      $routeProvider.
        when('/', {
          templateUrl: 'http://localhost:5000/static/app/templates/login.html',
          controller: 'loginController'
        }).
        when('/dashboard', {
          templateUrl: 'http://localhost:5000/static/app/templates/home.html',
          controller: 'dashboardController'
        }).
        when('/login', {
          template: '<phone-list></phone-list>'
        }).
        when('/signup', {
          template: '<phone-detail></phone-detail>'
        }).
        when('/upload', {
          templateUrl: 'http://localhost:5000/static/app/templates/upload.html',
          controller: 'uploadController'
        }).
        otherwise('/');

      // Configure all charts
      ChartJsProvider.setOptions({
        colours: ['#199C7B', '#FF8A80'],
        responsive: true
      });
      // Configure all line charts
      ChartJsProvider.setOptions('Line', {
        datasetFill: false
      });
    }
  ]);
