(function () {
  var app = angular.module("NYCTaxiAPP", ['ngRoute','ngMaterial','ngMap']);

  app.controller('AppCtrl', function($scope) {
    $scope.currentNavItem = 'page1';
    $scope.redirect1 = function() {
      window.location = "#/introduction";
    }
    $scope.redirect2 = function() {
      window.location = "#/predict";
    }
    $scope.redirect3 = function() {
      window.location = "#/charts";
    }
  });
  
})();