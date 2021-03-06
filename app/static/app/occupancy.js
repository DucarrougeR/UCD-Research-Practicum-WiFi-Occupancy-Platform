'use strict';
// TODO TEST all controllers are defined and various other parts. Check all views etc
var occupancyApp = angular.module('occupancyApp', [
    'ngRoute',
    'pikaday',
    'chart.js',
    'ngFileUpload',
]);

occupancyApp.controller('TopbarController', ['$scope', 'Authentication', 'Session', function($scope, Authentication, Session) {

    // console.log("checking");
    if (!Session.user) {
        console.log("checking auth");
        Authentication.getLoggedInUser().then(function(data) {

            Session.user = data;
            $scope.user = data;

        });
    } else {
      $scope.user = Session.user;
    }

    
}]);

occupancyApp.controller('DashboardController', ['$scope', '$http', 'Authentication', 'Session', 'RoomOccupancy', 'Permissions', function($scope, $http, Authentication, Session, RoomOccupancy, Permissions) {

    // check if there is a user defined
    if (!Session.user) {
        Authentication.getLoggedInUser().then(function(data) {

            Session.user = data;
            // make the hasPermission function available to templates
            $scope.hasPermission = Permissions.hasPermission;

        });
    } else {
        $scope.hasPermission = Permissions.hasPermission;
    }


    RoomOccupancy.getLeastUsed().then(function(data){
        if (data.length) {
            $scope.leastUsed = data;
        } else {
            $scope.message = "There are no rooms to display";
        }
    });

    RoomOccupancy.getMostUsed().then(function(data){
        if (data.length) {
            $scope.mostUsed = data;
        } else {
            $scope.message = "There are no rooms to display";
        }
    });
    
}]);


occupancyApp.controller('RoomsController', ['$scope', '$http', '$routeParams', 'Modules', 'Authentication', 'Session', 'DataManagement', 'Permissions', 'RoomOccupancy', function($scope, $http, $routeParams, Modules, Authentication, Session, DataManagement, Permissions, RoomOccupancy) {

    // check if there is a user defined
    if (!Session.user) {
        Authentication.getLoggedInUser().then(function(data) {

            Session.user = data;
            // make the hasPermission function available to templates
            $scope.hasPermission = Permissions.hasPermission;

        });
    } else {
        $scope.hasPermission = Permissions.hasPermission;
    }

    // get list of rooms
    RoomOccupancy.getRooms().then(function(resp){
      $scope.rooms = resp;
    });

    $scope.formData = {};
    if ($routeParams.room) {
        $scope.formData.room = $routeParams.room;
    }

    $scope.submit = function() {
        if ($scope.formData.room && $scope.formData.date && $scope.formData.type) {
            // formatting the URL
            var url = "/api/room/occupancy/" + $scope.formData.room + "/" + $scope.formData.date.split(" ").join("%20") + "/" + $scope.formData.type;
            
            $http.get(url).then(function successCallback(response) {

                if (response.data.results.length > 0) {

                    var results = DataManagement.organiseData(response.data.results, $scope.formData.type);

                    // bind the values
                    // $scope.maxValue = results["max"];
                    // $scope.minValue = results["min"];
                    // $scope.avgValue = Math.round(results["avg"] * 1000) / 1000;
                    // $scope.totalValue = results["hours"][0][0].room_capacity;
                    $scope.results = true;

                    // set the chart data
                    var resultsPercent = results["data"].map(function(i) {
                      return DataManagement.convertToPercent(i);
                    });
                    $scope.data = [resultsPercent];
                   
                    $scope.series = ['% occupied'];
                    console.log(results["hours"][0][0]);
                    $scope.score = DataManagement.convertToPercent(results["hours"][0][0]["room_occupancy_score"]);

                    // build the labels
                    $scope.labels = results["data"].map(function(item, index) {
                        return "Hour " + index;
                    });

                    $scope.options = {
                        responsive: true
                    }
                    $scope.onClick = function(points, evt) {
                        console.log(points, evt);
                    };

                    // for use in display messages
                    $scope.room = $scope.formData.room;
                    $scope.date = $scope.formData.date;
                    $scope.type = $scope.formData.type;


                    Modules.getModulesByRoom($scope.formData.room).then(function(modules) {
                        if (modules.results.length > 0) {

                            $scope.modules = modules.results;
                            console.log(modules.results.length);
                        }
                        
                    });



                } else {
                  $scope.results = false;
                  $scope.message = "No data available for " + $scope.formData.room + " on " + $scope.formData.date;
                }

                $scope.bannerType = "hidden";


            }, function errorCallback(response) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
            });
        } else {
            var errorMessage = "Please ensure these fields have been filled: ";
            if (!$scope.formData.type) {
                errorMessage += "type (binary or continuous) ,";
            }

            if (!$scope.formData.room) {
                errorMessage += "room ,";
            }

            if (!$scope.formData.date) {
                errorMessage += "a valid date ";
            }

            $scope.bannerType = "error";
            $scope.error = errorMessage;
        }
    }
}]);

occupancyApp.controller('ModulesController', ['$scope', '$http', '$routeParams', 'Authentication', 'Session', 'DataManagement', 'Permissions', 'Modules', function($scope, $http, $routeParams, Authentication, Session, DataManagement, Permissions, Modules) {

    // check if there is a user defined
    if (!Session.user) {
        Authentication.getLoggedInUser().then(function(data) {

            Session.user = data;
            // make the hasPermission function available to templates
            $scope.hasPermission = Permissions.hasPermission;

        });
    } else {
        $scope.hasPermission = Permissions.hasPermission;
    }

    Modules.getModulesList().then(function(data) {
        
        $scope.modules = data;
    });
    
    $scope.formData = {};

    $scope.submit = function() {
        if ($scope.formData.moduleSearch) {
            // formatting the URL
            var url = "/api/module/rooms-used/" + $scope.formData.moduleSearch;
            
            $http.get(url).then(function successCallback(response) {

                if (response.data.results.length > 0) {

                    $scope.results = response.data.results;

                } else {
                  $scope.results = false;
                  $scope.message = "No data available for " + $scope.formData.moduleSearch;
                }

                


            }, function errorCallback(response) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
            });
        }
    }

    if ($routeParams.module) {
        $scope.formData.moduleSearch = $routeParams.module;
        $scope.submit();
    }
}]);

// occupancyApp.controller("lineCtrl", ['$scope', '$timeout', 'chartData', function($scope, $timeout, chartData) {

//     //$scope.labels = ["07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"];
//     $scope.series = ['% occupied'];

//     // build the labels
//     $scope.labels = chartData.data.map(function(item, index) {
//         return "Hour " + index;
//     });

//     console.log("charting");
//     // get the data
//     $scope.data = [
//         chartData.data
//     ];
//     $scope.options = {
//         responsive: true
//     }
//     $scope.onClick = function(points, evt) {
//         console.log(points, evt);
//     };
// }]);


occupancyApp.controller("UploadController", ['$scope', 'Upload', '$timeout', 'Permissions', 'Session', 'Authentication', function($scope, Upload, $timeout, Permissions, Session, Authentication) {
    if (!Session.user) {
        Authentication.getLoggedInUser().then(function(data) {

            Session.user = data;
            // make the hasPermission function available to templates
            $scope.hasPermission = Permissions.hasPermission;

        });
    } else {
        $scope.hasPermission = Permissions.hasPermission;
    }

    $scope.$watch('files', function() {
        $scope.upload($scope.files);
    });
    $scope.$watch('file', function() {
        if ($scope.file != null) {
            $scope.files = [$scope.file];
        }
    });
    $scope.log = '';

    $scope.upload = function() {
        var files = $scope.files;
        if (files && files.length) {
            for (var i = 0; i < files.length; i++) {
                var file = files[i];
                if (!file.$error) {
                    // check an appropriate file type is selected
                    if ($scope.filetype == "wifi" || $scope.filetype == "truth" || $scope.filetype == "timetable") {
                        console.log($scope.filetype);
                        Upload.upload({
                            url: '/api/data/upload/' + $scope.filetype,
                            data: {
                                file: file
                            }
                        }).then(function(resp) {
                            $timeout(function() {
                                $scope.log = 'file: ' +
                                    resp.config.data.file.name +
                                    ', Response: ' + JSON.stringify(resp.data) +
                                    '\n' + $scope.log;
                            });

                            $scope.type = "success";
                            $scope.message = "File upload successful";
                        }, function(resp){
                            console.log("error");
                            $scope.type = "error";
                            $scope.message = "Invalid file type";
                        }, function(evt) {
                            var progressPercentage = parseInt(100.0 *
                                evt.loaded / evt.total);
                            $scope.log = 'progress: ' + progressPercentage +
                                '% ' + evt.config.data.file.name + '\n' +
                                $scope.log;
                            $scope.progress = progressPercentage;
                        });

                    } else {
                        $scope.type = "error";
                        
                        $scope.error = "Please Select an appropriate upload type";
                    }
                }
            }
        }
    };
}]);

occupancyApp.controller('AuthController', ['$scope', '$location', 'Authentication', 'Session', function($scope, $location, Authentication, Session) {
    $scope.error = "";
    $scope.submit = function() {
        var results = Authentication.loginUser($scope.email, $scope.password).then(function(data) {
            if (data.error) {
                $scope.error = data.error;
            } else {
                data['loggedIn'] = true;
                Session.user = data;
                console.log(Session.user);
                $location.path('/dashboard');
            }
        });

    }
}]);

occupancyApp.controller('RegisterController', ['$scope', 'Authentication', 'Permissions', 'Session', function($scope, Authentication, Permissions, Session) {
    // get possible permissions for a user
    Permissions.getPossiblePermissions().then(function(permissions) {

        $scope.permissions = permissions;
    });

    if (!Session.user) {
        Authentication.getLoggedInUser().then(function(data) {

            Session.user = data;
            // make the hasPermission function available to templates
            $scope.hasPermission = Permissions.hasPermission;

        });
    } else {
        $scope.hasPermission = Permissions.hasPermission;
    }


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
        }, function(error) {
            $scope.type = "error";
            $scope.message = data.data.error;
        });
    }
}]);

occupancyApp.controller('LogoutController', ['$scope', '$location', 'Authentication', 'Session', function($scope, $location, Authentication, Session) {
    Authentication.logoutUser().then(function(data) {
        Session.user = null;
        $location.path('/login');
    });

}]);

occupancyApp.filter('round2decimals', function() {
  return function(input) {
    return Math.round(input * 100) / 100;
  };
})
