// confirm all controllers are defined
describe('Authentication Service', function() {
    var redditService, httpBackend;

    beforeEach(module("Authentication"));

    beforeEach(inject(function(_Authentication_, $httpBackend) {
        Authentication = _Authentication_;
        httpBackend = $httpBackend;
    }));

    describe('Authentication getLoggedInUser', function() {

        it('should return a user object when a get request is made', function() {
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
                expect(user).toEqual({
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
        });

    });

    describe('Authentication getLoggedInUser', function() {

        it('should return a user object when a get request is made', function() {
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
                expect(user).toEqual({
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
        });

    });
});
