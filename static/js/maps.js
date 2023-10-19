function computeDensityFocus(pois) {
    let maxDensity = -Infinity;
    let bestPoi = null;

    pois.forEach((poi1) => {
        let count = 0;
        pois.forEach((poi2) => {
            // Compute Euclidean distance between two points
            let distance = Math.sqrt(Math.pow(poi1.lat - poi2.lat, 2) + Math.pow(poi1.lng - poi2.lng, 2));
            // If within a certain threshold, count it as nearby
            if(distance < 0.01) { // 0.01 is an arbitrary threshold; adjust based on your needs
                count++;
            }
        });
        if(count > maxDensity) {
            maxDensity = count;
            bestPoi = poi1;
        }
    });

    return bestPoi;
}

function initMap() {
    // Determine the POI with the highest density of nearby POIs
    let highestDensityPoi = computeDensityFocus(pois);

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 14,
        center: highestDensityPoi
    });

    // Color palette
    var colorPalette = ["#FF5733", "#33FF57", "#57C7FF", "#FFC457", "#9400D3", "#4B0082", "#FFD700", "#20B2AA", "#FF6347", "#7FFF00"];
    // Dynamically generate colors for each unique label
    var uniqueLabels = [...new Set(pois.map(poi => poi.label))];
    var colors = {};
    uniqueLabels.forEach((label, index) => {
        colors[label] = colorPalette[index % colorPalette.length];
    });

    pois.forEach(function(poi) {
        var color = colors[poi.label];
        var circle = {
            path: google.maps.SymbolPath.CIRCLE,
            fillColor: color,
            fillOpacity: 1,
            scale: 8,
            strokeColor: 'white',
            strokeWeight: 2
        };

        var marker = new google.maps.Marker({
            position: poi,
            map: map,
            icon: circle
        });

        var infowindow = new google.maps.InfoWindow({
            content: poi.info,
            pixelOffset: new google.maps.Size(0,10) // Adjusts the position of the infowindow
        });

        marker.addListener('mouseover', function() {
            infowindow.open(map, marker);
        });
        marker.addListener('mouseout', function() {
            infowindow.close();
        });
    });

    // Legend
    var legend = document.getElementById('legend');
    for (var key in colors) {
        var div = document.createElement('div');
        div.innerHTML = '<span style="background-color:' + colors[key] + '; padding: 10px; margin: 2px; display: inline-block;"></span> ' + key;
        legend.appendChild(div);
    }
    map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(legend);
}
