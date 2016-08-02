occupancyApp.factory('Authentication', ['$http', 'Session', function($http, Session){
	var currentUser;
	return {
		getCurrentUser: function() {
			return currentUser;
		},
		getLoggedInUser: function() {
			console.log("auth");
			console.log(this);
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

		registerUser: function (email, password) {
			$http({
				method: 'POST',
				data: {
					"email": email,
					"password": password
				},
				headers: {'Content-Type': 'application/x-www-form-urlencoded'},
				url: '/api/auth/register'
			}).then(function successCallback(response) {
				// this callback will be called asynchronously
				// when the response is available
				user = response.data;
				return JSON.parse(response);
			}, function errorCallback(response) {
				// called asynchronously if an error occurs
				// or server returns response with an error status.
				return JSON.parse(response);
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

		hasPermission: function(permission) {
			// if (user) {

			// }
		}
	}
}]);