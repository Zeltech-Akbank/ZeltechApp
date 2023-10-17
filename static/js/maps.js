  function initMap() {

    var myLatLng = { lat: 39.9334, lng: 32.8597 }; // LATITUDE ve LONGITUDE yerlerine istediğiniz koordinatları girin.

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 16,
        center: myLatLng
    });

    var hospitalIcon = {
        url: "https://maps.google.com/mapfiles/kml/shapes/hospitals.png", // Hastane simgesi
        scaledSize: new google.maps.Size(24, 24) // Boyutunu ayarlayın
    };

    var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        icon: hospitalIcon,
        title: 'Hastane'
    });
}