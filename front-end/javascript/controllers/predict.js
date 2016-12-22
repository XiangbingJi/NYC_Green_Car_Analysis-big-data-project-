angular.module('NYCTaxiAPP')
.controller('predictCtrl', function($scope,$http) {

    $scope.items = [
    "00:00 - 01:00", 
    "01:00 - 02:00", 
    "02:00 - 03:00", 
    "03:00 - 04:00", 
    "04:00 - 05:00", 
    "05:00 - 06:00", 
    "06:00 - 07:00",
    "07:00 - 08:00",
    "08:00 - 09:00",
    "09:00 - 10:00", 
    "10:00 - 11:00", 
    "11:00 - 12:00", 
    "12:00 - 13:00", 
    "13:00 - 14:00", 
    "14:00 - 15:00", 
    "15:00 - 16:00",
    "16:00 - 17:00",
    "17:00 - 18:00",
    "18:00 - 19:00", 
    "19:00 - 20:00", 
    "20:00 - 21:00", 
    "21:00 - 22:00", 
    "22:00 - 23:00", 
    "23:00 - 24:00", 
    ];
    $scope.selectedItem;
    $scope.getSelectedText = function() {
      if ($scope.selectedItem !== undefined) {
        return "You have selected: time  " + $scope.selectedItem;
      } else {
        return "Please select a time";
      }
    };
    $scope.latlng = [40.791, -73.947];
    $scope.getpos = function(event){
        $scope.latlng = [event.latLng.lat(), event.latLng.lng()];
        var location = $scope.latlng;
        console.log(location);
        $scope.latitude = location[0];
        $scope.longitude = location[1];
    };
    $scope.submit = function() {
        var longitude = $scope.longitude;
        var latitude = $scope.latitude;
        var timeZone =  $scope.items.indexOf($scope.selectedItem);
        $http.get('/GMM.json').success(function(data) {
            var GMM = data[timeZone];
            console.log(GMM);
            var coordinates = [];
            var dis = []
            for (i = 0; i < GMM.length; i++){
                coordinates.push(GMM[i]['coordinates']);
            }
            console.log(coordinates);
            for (i = 0; i < coordinates.length; i++){ 
                var distance = Math.sqrt((longitude - coordinates[i][0]) * (longitude - coordinates[i][0])  + (latitude - coordinates[i][1]) * (latitude - coordinates[i][1]));
                dis.push(distance);
            }
            var minIndex = indexOfMin(dis);
            var total = [66091, 49900, 69738, 24356, 21575, 16770, 22896, 40171, 58716, 60246, 55371, 56615, 57832, 58310, 67355, 74096, 78908, 85783, 94628, 89682, 68142, 71992, 74337, 76085];
           
            console.log(minIndex);

            var gaussian = GMM[minIndex]

            var temp =  total[timeZone] * integral(longitude - 0.005, latitude - 0.005, longitude + 0.005, latitude + 0.005, 20, gaussian) * gaussian.mag;
            console.log(total[timeZone]);
            console.log(temp);
            console.log('mag');
            console.log(gaussian.mag);
            $scope.pickups = temp;
        });
    };

    function func(x, y, gaussian){
        var mu1 = gaussian.coordinates[0];
        var mu2 = gaussian.coordinates[1];
        var matrix = gaussian.sigma;
        var sigma1 = Math.sqrt(matrix[0][0]);
        var sigma2 = Math.sqrt(matrix[1][1]);
        var p = matrix[0][1] / sigma1 / sigma2;
        //console.log(mu1,mu2,sigma1,sigma2,p);
        var A = 1/(2*Math.PI*sigma1*sigma2*Math.sqrt(1 - p * p));
        var B = Math.exp(-1/(2*(1 - p*p))*(Math.pow((x - mu1),2)/Math.pow(sigma1,2) + Math.pow(y - mu2, 2)/Math.pow(sigma2, 2) - 2*p*(x - mu1)*(y - mu2)/sigma1/sigma2));
        //console.log(A);
        //console.log(B);
        //console.log(A*B);
        return A*B;
    };

    function integral(x1,y1,x2,y2,n,gaussian){
        var dx = (x2 - x1)/n;
        var dy = (y2 - y1)/n;
        var sum = 0;

        console.log('debug1');
        console.log(dx);
        console.log(dy);
        for (var i = 0; i < n; i++){
            var x = x1 + i * dx;
            //console.log('x');
            //console.log(x);
            for (var j = 0; j < n; j++){
                var y = y1 + i * dy;
                var funVal = func(x, y, gaussian);
                //console.log(dx*dy*funVal);
                sum += dx * dy * funVal;
            }
        }
        console.log(sum);
        return sum;
    };

    function indexOfMin(arr) {
        if (arr.length === 0) {
            return -1;
        }
        var min = arr[0];
        var minIndex = 0;
        for (var i = 1; i < arr.length; i++) {
            if (arr[i] < min) {
                minIndex = i;
                min = arr[i];
            }
        }
        return minIndex;
    };

});
