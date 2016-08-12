occupancyApp.directive('logged-in-user', ['Session', function(Session) {
	
  return {
    template: '<div class="u-pull-left" >{{ user.email }}</div>\
    				<ul class="u-pull-left" >\
                    	<li ><a ng-href="/#/logout">Logout</a></li>\
                	</ul>',
    scope: {
      user: Session.user
    },
    replace: true
  };
}]);