occupancyApp.service('RoomOccupancy', ['$http', function($http, Session){
	var currentUser;
	return {
		getRooms: function(){
			return $http({
				method: 'GET',
				url: '/api/rooms/list'
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
}]);