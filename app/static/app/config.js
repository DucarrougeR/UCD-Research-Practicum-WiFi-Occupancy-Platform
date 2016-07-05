'use strict';

angular.
  module('occupancyApp').
  config(['$locationProvider' ,'$routeProvider', 'ChartJsProvider',
    function config($locationProvider, $routeProvider, ChartJsProvider) {
      $locationProvider.hashPrefix('!');

      $routeProvider.
        when('/login', {
          template: '<phone-list></phone-list>'
        }).
        when('/signup', {
          template: '<phone-detail></phone-detail>'
        }).
        otherwise('/');

      // Configure all charts
      ChartJsProvider.setOptions({
        colours: ['#FF5252', '#FF8A80'],
        responsive: false
      });
      // Configure all line charts
      ChartJsProvider.setOptions('Line', {
        datasetFill: false
      });
    }
  ]);
