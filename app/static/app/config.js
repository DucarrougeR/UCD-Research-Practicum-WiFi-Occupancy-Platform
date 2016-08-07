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
  ]);
