'use strict';

var occupancyApp = angular.module('occupancyApp', [
  'ngRoute',
  'pikaday',
  'chart.js',
  'ngFileUpload'
]);

occupancyApp.controller('DashboardController', ['$scope', '$http', 'chartData', 'Authentication', 'Session', 'DataManagement', 'Permissions', function($scope, $http, chartData, Authentication, Session, DataManagemen, Permissions) {
    $scope.message = "Hello Admin";

    // make the hasPermission function available to templates
    $scope.hasPermission = Permissions.hasPermission;
    // if there is no current user
    if (!Session.user) {
      Authentication.getLoggedInUser().then(function(data) {
        // Session service is shared between controllers to keep track of the current user
        Session.user = data;
      });
    } 

    // TODO: move this to a service or something
    $scope.submit = function() {
      if ($scope.formData.room && $scope.formData.date) {
        // formatting the URL
        var url = "/api/room/occupancy/"+ $scope.formData.room +"/" + $scope.formData.date.split(" ").join("%20");
        console.log("making request to " + url);
        $http.get(url).then(function successCallback(response) {
          
          
          if (response.data.results.length > 0) {
            

            var results = DataManagement.organiseData(response.data.results);

            // bind the values
            $scope.maxValue = results["max"];
            $scope.minValue = results["min"];
            $scope.avgValue = Math.round(results["avg"] * 1000) / 1000 ;
            $scope.totalValue = results["hours"][0][0].room_capacity;
            
            // set the chart data
            $scope.data = [results["data"]];
            $scope.series = ['% occupied'];

            // build the labels
            $scope.labels = results["data"].map(function(item, index) {
              return "Hour " + index;
            });
          }
          
          $scope.options = {
            responsive: true
          }
          $scope.onClick = function (points, evt) {
            console.log(points, evt);
          };

          
        }, function errorCallback(response) {
          // called asynchronously if an error occurs
          // or server returns response with an error status.
        });
      }
    }
}]);

occupancyApp.controller("lineCtrl", ['$scope', '$timeout', 'chartData', function ($scope, $timeout, chartData) {

  //$scope.labels = ["07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"];
  $scope.series = ['% occupied'];

  // build the labels
  $scope.labels = chartData.data.map(function(item, index) {
    return "Hour " + index;
  });

  console.log("charting");
  // get the data
  $scope.data = [
    chartData.data
  ];
  $scope.options = {
    responsive: true
  }
  $scope.onClick = function (points, evt) {
    console.log(points, evt);
  };
}]);


occupancyApp.controller("UploadController", ['$scope', 'Upload', '$timeout', function ($scope, Upload, $timeout) {
    $scope.$watch('files', function () {
        $scope.upload($scope.files);
    });
    $scope.$watch('file', function () {
        if ($scope.file != null) {
            $scope.files = [$scope.file]; 
        }
    });
    $scope.log = '';

    $scope.upload = function (files) {
        if (files && files.length) {
            for (var i = 0; i < files.length; i++) {
              var file = files[i];
              if (!file.$error) {
                Upload.upload({
                    url: '/api/data/upload',
                    data: {
                      username: $scope.username,
                      file: file  
                    }
                }).then(function (resp) {
                    $timeout(function() {
                        $scope.log = 'file: ' +
                        resp.config.data.file.name +
                        ', Response: ' + JSON.stringify(resp.data) +
                        '\n' + $scope.log;
                    });
                }, null, function (evt) {
                    var progressPercentage = parseInt(100.0 *
                        evt.loaded / evt.total);
                    $scope.log = 'progress: ' + progressPercentage + 
                      '% ' + evt.config.data.file.name + '\n' + 
                      $scope.log;
                });
              }
            }
        }
    };
}]);

occupancyApp.controller('AuthController', ['$scope', '$location', 'Authentication', 'Session', function($scope, $location, Authentication, Session){
  $scope.error = "";
  $scope.submit = function() {
      var results = Authentication.loginUser($scope.email, $scope.password).then(function(data) {
        if (data.error) {
          $scope.error = data.error;
        } else {
          data['loggedIn'] = true;
          Session.user = data;
          $location.path('/dashboard');
        }
      });
      
  }
}]);

occupancyApp.controller('RegisterController', ['$scope', 'Authentication', 'Permissions', function($scope, Authentication, Permissions){
  // get possible permissions for a user
  Permissions.getPossiblePermissions().then(function(permissions) {
    
    $scope.permissions = permissions;
  });
  

  $scope.submit = function() {
      Authentication.registerUser($scope.email, $scope.permission).then(function(data) {
        if (data.data.success) {
          // successful
          $scope.type = "success";
          $scope.message = data.data.success;
          $scope.email = "";
        } else {
          //failure
          $scope.type = "error";
          $scope.message = data.data.error;
        }
      });
    }
}]);
