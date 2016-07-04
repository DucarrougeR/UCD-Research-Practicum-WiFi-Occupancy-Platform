'use strict';

angular.
  module('occupancyApp').
  config(['$locationProvider' ,'$routeProvider',
    function config($locationProvider, $routeProvider) {
      $locationProvider.hashPrefix('!');

      $routeProvider.
        when('/login', {
          template: '<phone-list></phone-list>'
        }).
        when('/signup', {
          template: '<phone-detail></phone-detail>'
        }).
        otherwise('/');
    }
  ]);
