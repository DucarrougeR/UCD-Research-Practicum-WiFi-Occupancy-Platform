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
