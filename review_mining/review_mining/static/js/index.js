function initAutocomplete() {
  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -26.577419, lng: 0},
    zoom: 5,
    mapTypeId: 'roadmap'
  });

  // Create the search box and link it to the UI element.
  var input = document.getElementById('search_input');
  var searchBox = new google.maps.places.SearchBox(input);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  // Bias the SearchBox results towards current map's viewport.
  map.addListener('bounds_changed', function() {
    searchBox.setBounds(map.getBounds());
  });

  var markers = [];
  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener('places_changed', function() {
    var places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }

    // Clear out the old markers.
    markers.forEach(function(marker) {
      marker.setMap(null);
    });
    markers = [];

    // For each place, get the icon, name and location.
    var bounds = new google.maps.LatLngBounds();
    places.forEach(function(place) {
      console.log(place);
      name = place.name;
      type = place.types[0];
      lat = parseFloat(place.geometry.location['lat']());
      lng = parseFloat(place.geometry.location['lng']());
      //alert(name + " - Type: " + place.types.join(",") + ", Latitude: " + lat + ", Longitude: " + lng)
      

      var panorama = new google.maps.StreetViewPanorama(
      document.getElementById('map'), {
          position: {lat: lat, lng: lng},
          pov: {
            heading: 0,
            pitch: 0
          }
        });
      //map.setStreetView(panorama);
      $("#map").remove();
      
      var csrf = $("#csrf_token").find("input").val();
      $.ajax({
        type: "POST",
        url: "review_mining/get_reviews",
        data: { name: name, lat: lat, lng: lng, csrfmiddlewaretoken: csrf },
        success: function(response){
          $("#reviews").html(response);
          $("#reviews").show();
          console.log(response);
        }
      });
    });
  });
}