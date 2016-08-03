'use strict';

occupancyApp.config(['$locationProvider' ,'$routeProvider', '$logProvider', 'ChartJsProvider',
  function config($locationProvider, $routeProvider, $logProvider, ChartJsProvider) {
    $logProvider.debugEnabled(true);

    $routeProvider.
      when('/', {
        templateUrl: '/static/app/templates/login.html',
        controller: 'AuthController'
      }).
      when('/dashboard', {
        templateUrl: '/static/app/templates/home.html',
        controller: 'DashboardController'
      }).
      when('/login', {
        templateUrl: '/static/app/templates/login.html',
        controller: 'AuthController'
      }).
      when('/signup', {
        template: '<phone-detail></phone-detail>'
      }).
      when('/upload', {
        templateUrl: '/static/app/templates/upload.html',
        controller: 'UploadController'
      }).
      when('/add/user', {
        templateUrl: '/static/app/templates/add-user.html',
        resolve:{
          "check":function(Permissions,$location){   //function to be resolved, accessFac and $location Injected
            Permissions.hasPermission("add-user").then(function(data){
              if (data) {
                return true;
              } else {
                $location.path('/');                //redirect user to home if it does not have permission.
                alert("You don't have access here");
              }
            });
            
          }
        },
        controller: 'RegisterController'
      }).
      when('/add/ground-truth', {
        templateUrl: '/static/app/templates/add-truth.html',
        resolve:{
          "check":function(Permissions,$location){   //function to be resolved, accessFac and $location Injected
            if(Permissions.hasPermission("add-truth")){    //check if the user has permission -- This happens before the page loads
                return true;
            }else{
              $location.path('/');                //redirect user to home if it does not have permission.
              alert("You don't have access here");
            }
          }
        }
      }).
      when('/add/class', {
        templateUrl: '/static/app/templates/add-class.html',
        resolve:{
          "check":function(Permissions,$location){   //function to be resolved, accessFac and $location Injected
            Permissions.hasPermission("add-class").then(function(data){
              console.log(data);
              if (data) {

              } else {
                console.log('no permission');
              }
            });
            
          }
        }
      })

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
