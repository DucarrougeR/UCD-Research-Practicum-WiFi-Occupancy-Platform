// confirm all controllers are defined
describe('Authentication Service', function() {
    var Authentication, httpBackend;

    beforeEach(module("occupancyApp"));

    beforeEach(inject(function($injector, _Authentication_) {
        Authentication = _Authentication_;
        httpBackend = $injector.get('$httpBackend');
    }));

    describe('Authentication getLoggedInUser', function() {
        it('should return a user object when a get request is made', inject(function($httpBackend, geoProvider){
        	var httpBackend = $httpBackend;
            httpBackend.whenGET("/api/auth/current-user").respond({
                data: {
                    email: "admin@admin.com",
                    group: "admin",
                    permissions: {
                        "add-class": false,
                        "add-logs": true,
                        "add-truth": true,
                        "add-user": true,
                        "view-data": true
                    }
                }
            });

            Authentication.getLoggedInUser().then(function(user) {

                expect(user.data).toEqual({
                    email: "admin@admin.com",
                    group: "admin",
                    permissions: {
                        "add-class": false,
                        "add-logs": true,
                        "add-truth": true,
                        "add-user": true,
                        "view-data": true
                    }
                });
            });

            httpBackend.flush();
        }));

    });

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
});
