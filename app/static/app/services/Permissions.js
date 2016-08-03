occupancyApp.service('Permissions', ['$http', 'Session', 'Authentication', function($http, Session, Authentication) {
    return {
        hasPermission: function(permission) {
            // if the user has already been logged in
            if (Session.user) {
                // check their permissions
                if (Session.user.permissions[permission]) {
                    return true;
                }
            } else {
                // otherwise, get the current logged in user
                return Authentication.getLoggedInUser().then(function(data) {
                    console.log("user doesn't exists");
                    if (data.permissions[permission]) {
                        return true;
                    }
                });
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
