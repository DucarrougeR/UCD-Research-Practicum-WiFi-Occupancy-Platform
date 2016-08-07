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