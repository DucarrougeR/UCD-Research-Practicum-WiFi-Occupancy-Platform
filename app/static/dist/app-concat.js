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

occupancyApp.service('Authentication', ['$http', function($http, Session){
	var currentUser;
	return {
		getLoggedInUser: function() {
			return $http({
				method: 'GET',
				url: '/api/auth/current-user'
			}).then(function successCallback(response) {
				// this callback will be called asynchronously
				// when the response is available
				var user = this.currentUser = response.data;
				return user;
			}, function errorCallback(response) {
				// called asynchronously if an error occurs
				// or server returns response with an error status.
				return JSON.parse(response);
			});
		},

		registerUser: function (email, permission) {
			return $http({
				method: 'POST',
				data: {
					"email": email,
					"permission": permission
				},
				url: '/api/auth/register'
			}).then(function successCallback(response) {
				// this callback will be called asynchronously
				// when the response is available
				return response;
				// user = response.data;
				// return JSON.parse(response);
			}, function errorCallback(response) {
				// called asynchronously if an error occurs
				// or server returns response with an error status.
				return response;
			});
		},

		loginUser: function (email, password) {
			return $http({
				method: 'POST',
				data: {
					"email": email,
					"password": password
				},
				url: '/api/auth/login'
			}).then(function successCallback(response) {
				this.user = response.data;
				return response.data;
			}, function errorCallback(response) {
				return response.data;
			});
		}, 

		logoutUser: function() {
			return $http({
				method: 'GET',
				url: '/api/auth/logout'
			}).then(function successCallback(response) {
				
				return true;
				
			}, function errorCallback(response) {
				
				return false;
			});
		}
	}
}]);
occupancyApp.service('Session', [function(){
	this.user = null;
	this.isUserLoggedIn = function(){
		if (this.user) {
			return this.user;
		} else {
			return false;
		}
	}
}])
occupancyApp.service('Permissions', ['$http', 'Session', 'Authentication', function($http, Session, Authentication) {
    return {
        hasPermission: function(permission, type) {
            // if the user has already been logged in
            if (Session.user) {
                // check their permissions
                if( Object.prototype.toString.call( permission ) === '[object Array]' ) {
                    // iterate through each item
                    for (var i = 0; i < permission.length; i++) {
                        // if type is AND then user requires all the permissions. Exit if they don't have one of them
                        if (type == "AND") {
                            if (!Session.user.permissions[i]) {
                                return false;
                            } 
                        } else if (type == "OR") {
                            // if user has any of the listed permissions, then return true
                            if (Session.user.permissions[i]) {
                                return true;
                            } 
                        }
                    }
                } else {
                    // otherwise, single permission passed and so return true if they have it and false if they don't
                    return Session.user.permissions[permission]  
                }
                
            } 
            
            return false;
        },

        getPossiblePermissions: function() {
            return $http({
                method: 'GET',
                url: '/api/auth/permissions/get-all'
            }).then(function successCallback(response) {
                // this callback will be called asynchronously
                // when the response is available
                return response.data;
                // user = response.data;
                // return JSON.parse(response);
            }, function errorCallback(response) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
                return response.data;
            });
        }
    }

}])


occupancyApp.service('DataManagement', [function() {
    // TODO TEST organiseData function
    return {
        organiseData: function(results, type) {
            
            var hours = [];
            // separates results into unique hours
            results.map(function(item, index) {
                var subStr = item.counts_time.substring(11, 13) * 1
                    // if the hour has already been listed then push it onto the hours array at a specific index
                if (hours[subStr]) {
                    hours[subStr].push(item);
                } else {
                    hours[subStr] = [item];
                }

            });

            var min = hours[0][0].room_capacity;
            var max = 0;

            // cycle through each hour
            var reducedData = hours.map(function(item) {

                // reduce the items to a single total value
                var reduced = item.reduce(function(total, i) {
                    // if (i.counts_authenticated > max) {
                    //     max = i.counts_authenticated;
                    // }

                    // if (i.counts_authenticated < min) {
                    //     min = i.counts_authenticated;
                    // }
                    if (type=="binary") {
                        return (total || i.counts_predicted_is_occupied);
                        
                    } else {
                        
                        return (total + (i.counts_predicted / i.room_capacity/ 1));
                    }
                    
                }, 0);

                
                // return the average
                if (type=="binary") {
                    return reduced;
                }
                return reduced / item.length
            });

            // var avg = reducedData.reduce(function(total, i) {
              
            //   return total + i;
            // }) / reducedData.length;

            // return results
            returnResults = {
              "data": reducedData,
              "hours": hours
            };
            
            return returnResults;
        },

        convertToPercent: function(value) {
            return Math.round(value*10000)/100;
        }
    }

}])

occupancyApp.service('RoomOccupancy', ['$http', function($http, Session){
	var currentUser;
	return {
		getRooms: function(){
			return $http({
				method: 'GET',
				url: '/api/rooms/list'
			}).then(function successCallback(response) {
				// this callback will be called asynchronously
				// when the response is available
				return response.data;
				// user = response.data;
				// return JSON.parse(response);
			}, function errorCallback(response) {
				// called asynchronously if an error occurs
				// or server returns response with an error status.
				return response.data;
			});
		},
		getLeastUsed: function() {
			return $http({
				method: 'GET',
				url: '/api/rooms/usage/least'
			}).then(function successCallback(response) {
				// this callback will be called asynchronously
				// when the response is available
				return response.data;
				// user = response.data;
				// return JSON.parse(response);
			}, function errorCallback(response) {
				// called asynchronously if an error occurs
				// or server returns response with an error status.
				return response.data;
			});
		},
		getMostUsed: function() {
			return $http({
				method: 'GET',
				url: '/api/rooms/usage/most'
			}).then(function successCallback(response) {
				// this callback will be called asynchronously
				// when the response is available
				
				return response.data;
				// user = response.data;
				// return JSON.parse(response);
			}, function errorCallback(response) {
				// called asynchronously if an error occurs
				// or server returns response with an error status.
				return response.data;
			});
		}
		
	}
}]);
occupancyApp.service('Modules', ['$http', 'Session', 'Authentication', function($http, Session, Authentication) {
    return {
        getModulesList: function() {
            return $http({
                method: 'GET',
                url: '/api/module/list'
            }).then(function successCallback(response) {
                // this callback will be called asynchronously
                // when the response is available

                return response.data;
                // user = response.data;
                // return JSON.parse(response);
            }, function errorCallback(response) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
                return response.data;
            });
        },

        getModulesByRoom: function(room) {
            return $http({
                method: 'GET',
                url: '/api/module/room/' + room
            }).then(function successCallback(response) {
                // this callback will be called asynchronously
                // when the response is available
                console.log(response);
                return response.data;
                // user = response.data;
                // return JSON.parse(response);
            }, function errorCallback(response) {
                // called asynchronously if an error occurs
                // or server returns response with an error status.
                return response.data;
            });
        }
    }

}])

'use strict';

occupancyApp.config(['$locationProvider' ,'$routeProvider', '$logProvider', 'ChartJsProvider',
  function config($locationProvider, $routeProvider, $logProvider, ChartJsProvider) {
    $logProvider.debugEnabled(true);

    $routeProvider.
      when('/', {
        templateUrl: '/static/app/templates/login.html',
        controller: 'AuthController',
        resolve: {
          "check":function(Permissions,Session, Authentication, $location){   //function to be resolved, accessFac and $location Injected
            if (!Session.user) {
              Authentication.getLoggedInUser().then(function(data) {
                // if the user is logged in
                if (data) {
                  // redirect to dashboard
                  $location.path("/dashboard");
                } else {
                  // if not logged in
                  // redirect to login
                  $location.path("/login");

                }

              });
            } else {
              // user is logged in
              // redirect to dashboard
              $location.path("/dashboard");

            }
            
          }
        }
      }).
      when('/dashboard', {
        templateUrl: '/static/app/templates/home.html',
        resolve:{
          "check":function(Permissions,Session, Authentication, $location){   //function to be resolved, accessFac and $location Injected
            if (!Session.user) {
              Authentication.getLoggedInUser().then(function(data) {
                if (data) {
                  return true;
                } else {
                  $location.path("/login");
                }

              });
            } else {
              return true;
            }
            
          }
        },
        controller: 'DashboardController',

      }).

      when('/rooms', {
        templateUrl: '/static/app/templates/rooms.html',
        resolve:{
          "check":function(Permissions,Session, Authentication, $location){   //function to be resolved, accessFac and $location Injected
            if (!Session.user) {
              Authentication.getLoggedInUser().then(function(data) {
                if (data) {
                  return true;
                } else {
                  $location.path("/login");
                }

              });
            } else {
              return true;
            }
            
          }
        },
        controller: 'RoomsController',

      }).
      when('/rooms/:room', {
        templateUrl: '/static/app/templates/rooms.html',
        resolve:{
          "check":function(Permissions,Session, Authentication, $location){   //function to be resolved, accessFac and $location Injected
            if (!Session.user) {
              Authentication.getLoggedInUser().then(function(data) {
                if (data) {
                  return true;
                } else {
                  $location.path("/login");
                }

              });
            } else {
              return true;
            }
            
          }
        },
        controller: 'RoomsController',

      }).
      when('/modules', {
        templateUrl: '/static/app/templates/modules.html',
        resolve:{
          "check":function(Permissions,Session, Authentication, $location){   //function to be resolved, accessFac and $location Injected
            if (!Session.user) {
              Authentication.getLoggedInUser().then(function(data) {
                if (data) {
                  return true;
                } else {
                  $location.path("/login");
                }

              });
            } else {
              return true;
            }
            
          }
        },
        controller: 'ModulesController',

      }).

      when('/modules/:module', {
        templateUrl: '/static/app/templates/modules.html',
        resolve:{
          "check":function(Permissions,Session, Authentication, $location){   //function to be resolved, accessFac and $location Injected
            if (!Session.user) {
              Authentication.getLoggedInUser().then(function(data) {
                if (data) {
                  return true;
                } else {
                  $location.path("/login");
                }

              });
            } else {
              return true;
            }
            
          }
        },
        controller: 'ModulesController',

      }).
      when('/login', {
        templateUrl: '/static/app/templates/login.html',
        controller: 'AuthController'
      }).
      when('/upload', {
        templateUrl: '/static/app/templates/upload.html',
        resolve:{
          "check":function(Permissions,Session, Authentication, $location){   //function to be resolved, accessFac and $location Injected
            if (!Session.user) {
              Authentication.getLoggedInUser().then(function(data) {
                if (Permissions.hasPermission(["add-truth", "add-logs", "add-class"], "OR")) {
                  return true;
                }
                return false;

              });
            } else {
              if (Permissions.hasPermission(["add-truth", "add-logs", "add-class"], "OR")) {
                  return true;
                }
                return false;
            }
            
          }
        },
        controller: 'UploadController'
      }).
      when('/add/user', {
        templateUrl: '/static/app/templates/add-user.html',
        resolve:{
          "check":function(Permissions,Session, Authentication, $location){   //function to be resolved, accessFac and $location Injected
            if (!Session.user) {
              Authentication.getLoggedInUser().then(function(data) {
                if (Permissions.hasPermission("add-user")) {
                  return true;
                }
                return false;
                

              });
            } else {
              if (Permissions.hasPermission("add-user")) {
                  return true;
                }
                return false;
            }
            
            
          }
        },
        controller: 'RegisterController'
      }).
      when('/add/ground-truth', {
        templateUrl: '/static/app/templates/add-truth.html',
        resolve:{
          "check":function(Permissions,Session, Authentication,$location){   //function to be resolved, accessFac and $location Injected
            if (!Session.user) {
              Authentication.getLoggedInUser().then(function(data) {
                
                if (Permissions.hasPermission("add-truth")) {
                  return true;
                }
                return false;

              });
            } else {
              if (Permissions.hasPermission("add-truth")) {
                  return true;
                }
                return false;
            }
          }
        }
      }).
      when('/add/class', {
        templateUrl: '/static/app/templates/add-class.html',
        resolve:{
          "check":function(Permissions,Session, Authentication,$location){   //function to be resolved, accessFac and $location Injected
            if (!Session.user) {
              Authentication.getLoggedInUser().then(function(data) {
                
                if (Permissions.hasPermission("add-class")) {
                  return true;
                }
                return false;
              });
            } else {
              if (Permissions.hasPermission("add-class")) {
                  return true;
                }
                return false;
            }
            
          }
        }
      }).
      when('/logout', {
        controller: "LogoutController",
        template: "<h1>Logging you out</h1>"
      });

    //$locationProvider.html5Mode(true);  

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
  ]).run(function($rootScope, $location, Session, Authentication) {
    // this runs before any routing
    $rootScope.$on( "$routeChangeStart", function(event, next, current) {
      
      if (!Session.user) {
        
        Authentication.getLoggedInUser().then(function(user) {

          Session.user = user;
          $rootScope.user = user;
          
        });
      } else {
        
        $rootScope.user = Session.user;
      }
    });
  });
