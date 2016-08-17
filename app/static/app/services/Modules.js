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
