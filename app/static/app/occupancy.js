'use strict';

var occupancyApp = angular.module('occupancyApp', [
  'ngRoute',
  'datePicker',
  'chart.js'
]);

occupancyApp.controller('primaryController', function($scope) {
    $scope.greeting = 'Hello';
});

occupancyApp.controller("lineCtrl", ['$scope', '$timeout', function ($scope, $timeout) {

  $scope.labels = ["07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"];
  $scope.series = ['% occupied'];
  $scope.data = [
    [65, 59, 80, 81, 56, 55, 40, 28, 48, 40, 19, 86, 27, 90]
  ];
  $scope.onClick = function (points, evt) {
    console.log(points, evt);
  };

  // Simulate async data update
  // $timeout(function () {
  //   $scope.data = [
  //     [28, 48, 40, 19, 86, 27, 90, 65, 59, 80, 81, 56, 55, 40]
  //   ];
  // }, 3000);

  //[28, 48, 40, 19, 86, 27, 90, 65, 59, 80, 81, 56, 55, 40]
  // [65, 59, 80, 81, 56, 55, 40, 28, 48, 40, 19, 86, 27, 90]
}]);
