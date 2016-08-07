occupancyApp.service('Session', [function(){
	this.user = null;
	this.isUserLoggedIn = function(){
		if (this.user) {
			return this.user;
		} else {
			return false;
		}
	}
}])