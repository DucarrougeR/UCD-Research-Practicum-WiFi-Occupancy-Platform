// confirm all controllers are defined
// describe('myApp.view2 module', function() {

//   beforeEach(module('myApp.view2'));

//   describe('view2 controller', function(){

//     it('should ....', inject(function($controller) {
//       //spec body
//       var view2Ctrl = $controller('View2Ctrl');
//       expect(view2Ctrl).toBeDefined();
//     }));

//   });
// });

// confirm all controllers are defined
// describe('Authentication Service', function() {
//     var Authentication;
//     var httpBackend;

//     beforeEach(angular.mock.module("occupancyApp"));

//     beforeEach(inject(function($injector, _Authentication_) {
//         Authentication = _Authentication_;
//         httpBackend = $injector.get('$httpBackend');
//     }));

//     describe('Authentication getLoggedInUser', function() {

//         it('should return a user object when a get request is made', inject(function($httpBackend, geoProvider){
//         	var httpBackend = $httpBackend;
//             httpBackend.whenGET("/api/auth/current-user").respond({
//                 data: {
//                     email: "admin@admin.com",
//                     group: "admin",
//                     permissions: {
//                         "add-class": false,
//                         "add-logs": true,
//                         "add-truth": true,
//                         "add-user": true,
//                         "view-data": true
//                     }
//                 }
//             });

//             Authentication.getLoggedInUser().then(function(user) {
//                 expect(user).toEqual({
//                     email: "admin@admin.com",
//                     group: "admin",
//                     permissions: {
//                         "add-class": false,
//                         "add-logs": true,
//                         "add-truth": true,
//                         "add-user": true,
//                         "view-data": true
//                     }
//                 });
//             });

//             httpBackend.flush();
//         }));

//     });

    // describe('Authentication getLoggedInUser', function() {

    //     it('should return a user object when a get request is made', function() {
    //         httpBackend.whenGET("/api/auth/current-user").respond({
    //             data: {
    //                 email: "admin@admin.com",
    //                 group: "admin",
    //                 permissions: {
    //                     "add-class": false,
    //                     "add-logs": true,
    //                     "add-truth": true,
    //                     "add-user": true,
    //                     "view-data": true
    //                 }
    //             }
    //         });

    //         Authentication.getLoggedInUser().then(function(user) {
    //             expect(user).toEqual({
    //                 email: "admin@admin.com",
    //                 group: "admin",
    //                 permissions: {
    //                     "add-class": false,
    //                     "add-logs": true,
    //                     "add-truth": true,
    //                     "add-user": true,
    //                     "view-data": true
    //                 }
    //             });
    //         });
    //     });

    // });
//});
