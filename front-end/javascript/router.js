angular.module('NYCTaxiAPP')
 .config(function($routeProvider){
  $routeProvider.when('/introduction',{
    templateUrl: 'templates/introduction.html',
    controller: 'introCtrl'
  })
  .when('/predict',{
    templateUrl: '/templates/predict.html',
    controller: 'predictCtrl'
  })
  .when('/charts',{
    templateUrl: '/templates/charts.html',
    controller: 'chartsCtrl'
  })
  .otherwise({ redirectTo: '/' });
})
