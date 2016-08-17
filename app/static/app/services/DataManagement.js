
occupancyApp.service('DataManagement', [function() {
    // TODO TEST organiseData function
    return {
        organiseData: function(results, type) {
            
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
                    // if (i.counts_authenticated > max) {
                    //     max = i.counts_authenticated;
                    // }

                    // if (i.counts_authenticated < min) {
                    //     min = i.counts_authenticated;
                    // }
                    if (type=="binary") {
                        return (total || i.counts_predicted_is_occupied);
                        
                    } else {
                        
                        return (total + (i.counts_predicted / i.room_capacity/ 1));
                    }
                    
                }, 0);

                
                // return the average
                if (type=="binary") {
                    return reduced;
                }
                return reduced / item.length
            });

            // var avg = reducedData.reduce(function(total, i) {
              
            //   return total + i;
            // }) / reducedData.length;

            // return results
            returnResults = {
              "data": reducedData,
              "hours": hours
            };
            
            return returnResults;
        },

        convertToPercent: function(value) {
            return Math.round(value*10000)/100;
        }
    }

}])
