'use strict';

var occupancyApp = angular.module('occupancyApp', [
  'ngRoute'
]);

occupancyApp.controller('primaryController', function($scope) {
    $scope.greeting = 'Hello';
});
