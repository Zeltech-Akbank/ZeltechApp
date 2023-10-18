function initMap() {
    var myLatLng = pois[0];

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 17,
        center: myLatLng
    });

    var colors = {
        'Hastane': "#FF5733",
        'Eczane': "#33FF57",
        'Park Alanı': "#57C7FF",
        'Veteriner': "#FF57A7",
        'Okul': "#A457FF"
    };

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
            icon: circle,
            title: poi.label
        });

        // Bilgi penceresi için
        var infowindow = new google.maps.InfoWindow({
            content: poi.info
        });

        marker.addListener('mouseover', function() {
            infowindow.open(map, marker);
        });
        marker.addListener('mouseout', function() {
            infowindow.close();
        });
    });

    // Efsane (legend) oluşturalım
    var legend = document.getElementById('legend');
    for (var key in colors) {
        var div = document.createElement('div');
        div.innerHTML = '<span style="background-color:' + colors[key] + '; padding: 10px; margin: 2px; display: inline-block;"></span> ' + key;
        legend.appendChild(div);
    }
    map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(legend);
}

$(document).off('click', '.duzenle').on('click', '.duzenle', function(event) {
    event.stopPropagation();

    let id = $(this).data('id');
    let teyit = $(`.teyit[data-id="${id}"]`).is(':checked') ? 'Evet' : 'Hayır';
    let karsilandi = $(`.karsilandi[data-id="${id}"]`).is(':checked') ? 'Evet' : 'Hayır';

    $.ajax({
        url: `/durum-duzenle/${id}`,
        method: 'POST',
        data: {
            teyit: teyit,
            karsilandi: karsilandi
        },
        success: function(response) {
            if (response.status === 'success') {
                alert('Değişiklikler başarıyla kaydedildi!');
            } else {
                alert('Bir hata oluştu.');
            }
        }
    });
});


function updateTable() {
    var searchValue = $("#searchInput").val().toLowerCase();

    var teyitChecked = $("#filterTeyit").is(':checked');
    var karsilandiChecked = $("#filterKarsilandi").is(':checked');

    $("tbody tr").each(function() {
        var currentRow = $(this);
        var teyitValue = currentRow.find('.teyit').prop('checked');
        var karsilandiValue = currentRow.find('.karsilandi').prop('checked');

        var rowText = currentRow.text().toLowerCase();
        var showRow = true;

        if (searchValue && !rowText.includes(searchValue)) {
            showRow = false;
        }

        if (teyitChecked && !teyitValue) {
            showRow = false;
        }

        if (karsilandiChecked && !karsilandiValue) {
            showRow = false;
        }

        if (showRow) {
            currentRow.show();
        } else {
            currentRow.hide();
        }
    });
}
