
occupancyApp.service('DataManagement', [function() {
    // TODO TEST organiseData function
    return {
        organiseData: function(results) {
            console.log(results);
            var hours = [];
            // separates results into unique hours
            results.map(function(item, index) {
                var subStr = item.counts_time.substring(11, 13) * 1
                    // if the hour has already been listed then push it onto the hours array at a specific index
                if (hours[subStr]) {
                    hours[subStr].push(item);
                } else {
                    hours[subStr] = [item];
                }

            });

            var min = hours[0][0].room_capacity;
            var max = 0;

            // cycle through each hour
            var reducedData = hours.map(function(item) {

                // reduce the items to a single total value
                var reduced = item.reduce(function(total, i) {
                    if (i.counts_authenticated > max) {
                        max = i.counts_authenticated;
                    }

                    if (i.counts_authenticated < min) {
                        min = i.counts_authenticated;
                    }

                    return (total + (i.counts_authenticated / 1))
                }, 0);

                // return the average
                return reduced / item.length
            });

            var avg = reducedData.reduce(function(total, i) {
              
              return total + i;
            }) / reducedData.length;

            // return results
            return {
              "min": min,
              "max": max,
              "avg": avg,
              "data": reducedData,
              "hours": hours
            }
        }
    }

}])
