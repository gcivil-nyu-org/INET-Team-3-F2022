const btn1BikeLane = document.getElementById("btn1");
const btn2BikePark = document.getElementById("btn2");
const btn3BikeColl = document.getElementById("btn3");
const btn4RepIssue = document.getElementById("btn4");
const btn5SeeEvnts = document.getElementById("btn5");

/*
  BUTTON 1: Bike Lanes
*/

btn1BikeLane.addEventListener("click", function onClick() {
  btn1BikeLane.classList.remove("btn-secondary");
  btn1BikeLane.classList.add("btn-primary");
  btn2BikePark.classList.remove("btn-primary");
  btn3BikeColl.classList.remove("btn-primary");
  btn4RepIssue.classList.remove("btn-primary");
  btn5SeeEvnts.classList.remove("btn-primary");
  btn2BikePark.classList.add("btn-secondary");
  btn3BikeColl.classList.add("btn-secondary");
  btn4RepIssue.classList.add("btn-secondary");
  btn5SeeEvnts.classList.add("btn-secondary");

  const uluru = { lat: 40.7237, lng: -73.9898 };

  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 15,
    center: uluru,
  });

  const bikeLayer = new google.maps.BicyclingLayer();
  bikeLayer.setMap(map);
});

function initMap() {
  const uluru = { lat: 40.7237, lng: -73.9898 };

  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 11,
    center: uluru,
  });

  const bikeLayer = new google.maps.BicyclingLayer();
  bikeLayer.setMap(map);
}

/*
  BUTTON 2: Bike Parking
*/

btn2BikePark.addEventListener("click", function onClick() {
  btn2BikePark.classList.remove("btn-secondary");
  btn2BikePark.classList.add("btn-primary");
  btn1BikeLane.classList.remove("btn-primary");
  btn3BikeColl.classList.remove("btn-primary");
  btn4RepIssue.classList.remove("btn-primary");
  btn5SeeEvnts.classList.remove("btn-primary");
  btn1BikeLane.classList.add("btn-secondary");
  btn3BikeColl.classList.add("btn-secondary");
  btn4RepIssue.classList.add("btn-secondary");
  btn5SeeEvnts.classList.add("btn-secondary");

  const uluru = { lat: 40.7237, lng: -73.9898 };

  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 15,
    center: uluru,
  });

  map.data.loadGeoJson(parkingGeoJson);

  map.data.setStyle(function (feature) {
    return {
      icon: markerpng,
    }
  });
});

/*
  BUTTON 3: Bike Collisions
*/

btn3BikeColl.addEventListener("click", function onClick() {
  btn3BikeColl.classList.remove("btn-secondary");
  btn3BikeColl.classList.add("btn-primary");
  btn1BikeLane.classList.remove("btn-primary");
  btn2BikePark.classList.remove("btn-primary");
  btn4RepIssue.classList.remove("btn-primary");
  btn5SeeEvnts.classList.remove("btn-primary");
  btn1BikeLane.classList.add("btn-secondary");
  btn2BikePark.classList.add("btn-secondary");
  btn4RepIssue.classList.add("btn-secondary");
  btn5SeeEvnts.classList.add("btn-secondary");

  const uluru = { lat: 40.7237, lng: -73.9898 };

  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 15,
    center: uluru,
  });

  map.data.setStyle(function (feature) {
    return {
      icon: markerpng,
    }
  });

  map.data.loadGeoJson(collisionsGeoJson);

  map.data.setStyle(function (feature) {
    return {
      icon: markerpng,
    }
  });

  var infowindow = new google.maps.InfoWindow();
  map.data.addListener("click", function (event) {
    let date = event.feature.getProperty("CRASH DATE");
    let time = event.feature.getProperty("CRASH TIME");
    let borough = event.feature.getProperty("BOROUGH");
    let zip = event.feature.getProperty("ZIP CODE");
    let numKilled = event.feature.getProperty("NUMBER OF CYCLIST KILLED");
    let numInjured = event.feature.getProperty(
      "NUMBER OF CYCLIST INJURED"
    );

    let html =
      "<b>Crash Date:</b> " + date + "<br>" +
      "<b>Crash Time (military time):</b> " + time + "<br>" +
      "<b>Borough:</b> " + borough + "<br>" +
      "<b>Zipcode:</b> " + zip + "<br>" +
      "<b>Cyclists Injured:</b> " + numInjured + "<br>" +
      "<b>Cyclists Killed:</b> " + numKilled + "<br>";
    infowindow.setContent(html);
    infowindow.setPosition(event.latLng);
    infowindow.setOptions({ pixelOffset: new google.maps.Size(0, -30) });
    infowindow.open(map);
  });
});

/*
  BUTTON 4: Reported Lane Issues
*/
btn4RepIssue.addEventListener("click", function onClick() {
  btn4RepIssue.classList.remove("btn-secondary");
  btn4RepIssue.classList.add("btn-primary");
  btn1BikeLane.classList.remove("btn-primary");
  btn2BikePark.classList.remove("btn-primary");
  btn3BikeColl.classList.remove("btn-primary");
  btn5SeeEvnts.classList.remove("btn-primary");
  btn1BikeLane.classList.add("btn-secondary");
  btn2BikePark.classList.add("btn-secondary");
  btn3BikeColl.classList.add("btn-secondary");
  btn5SeeEvnts.classList.add("btn-secondary");

  const uluru = { lat: 40.7237, lng: -73.9898 };

  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 15,
    center: uluru,
  });

  let locations = [];
  for (let i = 0; i < issueObjsJson.length; i++) {
    locations.push(issueObjsJson[i]['fields']['location']);
  }

  let issueInfos = [];
  for (let i = 0; i < issueObjsJson.length; i++) {
    issueInfos.push(issueObjsJson[i]['fields']);
  }

  var geocoder;
  geocoder = new google.maps.Geocoder();
  var markers_temp = []
  var markerClusterer = new MarkerClusterer(map, markers_temp,
    { zoomOnClick: false, imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m' });
  // Add some markers to the map.
  var markers = locations.map((location, i) => {
    const issueInfo = issueInfos[i % issueInfos.length];

    geocoder.geocode({ 'address': location }, function (results, status) {
      if (status === 'OK') {
        var marker = new google.maps.Marker({
          map: map,
          position: results[0].geometry.location,
        });

        const contentStr =
          '<div id="content">' +
          '<div id="siteNotice">' +
          "</div>" +
          '<h4 id="firstHeading" class="firstHeading">' + issueInfo['title'] + '</h4>' +
          '<div id="bodyContent">' +
          "<p>" + issueInfo['content'] + "</p>" +
          '<p>Author: ' + issueInfo['author'] + '</p>' +
          '<p>Location: ' + issueInfo['location'] + '</p>' +
          "</div>" +
          "</div>";
        var infoWindow = new google.maps.InfoWindow({
          content: contentStr
        });
        marker.addListener("click", () => {
          infoWindow.open(map, marker);
        });
        markers_temp.push(marker)
        markerClusterer.addMarker(marker);
      }

      else {
        console.log(location + ': Geocode was not successful for the following reason: ' + status);
      }
    });
  });

});

/*
  BUTTON 5: Events
*/
btn5SeeEvnts.addEventListener("click", function onClick() {
  btn5SeeEvnts.classList.remove("btn-secondary");
  btn5SeeEvnts.classList.add("btn-primary");
  btn1BikeLane.classList.remove("btn-primary");
  btn2BikePark.classList.remove("btn-primary");
  btn3BikeColl.classList.remove("btn-primary");
  btn4RepIssue.classList.remove("btn-primary");
  btn1BikeLane.classList.add("btn-secondary");
  btn2BikePark.classList.add("btn-secondary");
  btn3BikeColl.classList.add("btn-secondary");
  btn4RepIssue.classList.add("btn-secondary");

  const uluru = { lat: 40.7237, lng: -73.9898 };

  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 15,
    center: uluru,
  });

  let locations = [];
  for (let i = 0; i < publicObjsJson.length; i++) {
    locations.push(publicObjsJson[i]['fields']['location']);
  }

  let publicEventInfos = [];
  for (let i = 0; i < publicObjsJson.length; i++) {
    publicEventInfos.push(publicObjsJson[i]['fields']);
  }

  var geocoder;
  geocoder = new google.maps.Geocoder();
  var markers_temp = []
  let hmap = {};
  var markerClusterer = new MarkerClusterer(map, markers_temp,
    { zoomOnClick: false, imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m' });
  // Add some markers to the map.
  var markers = locations.map((location, i) => {
    const publicEventInfo = publicEventInfos[i % publicEventInfos.length];

    geocoder.geocode({ 'address': location }, function (results, status) {
      if (status === 'OK') {
        var marker = new google.maps.Marker({
          map: map,
          position: results[0].geometry.location,
        });

        const contentStr =
          '<div id="content">' +
          '<div id="siteNotice">' +
          "</div>" +
          '<h4 id="firstHeading" class="firstHeading">' + publicEventInfo['title'] + '</h4>' +
          '<div id="bodyContent">' +
          "<p>" + publicEventInfo['description'] + "</p>" +
          "<p>Event Type: " + publicEventInfo['event_type'] + "</p>" +
          '<p>Author: ' + publicEventInfo['created_by'] + '</p>' +
          '<p>Location: ' + publicEventInfo['location'] + '</p>' +
          "</div>" +
          "</div>";
        var infoWindow = new google.maps.InfoWindow({
          content: contentStr
        });
        marker.addListener("click", () => {
          infoWindow.open(map, marker);
        });
        markers_temp.push(marker)
        let latLngCheck = marker.getPosition().lat() + "," + marker.getPosition().lng();
        let lat1 = marker.getPosition().lat();
        let lng1 = marker.getPosition().lng();
        latLngCheck = lat1 + "," + lng1;
        if (hmap[latLngCheck]) {
          while (hmap[latLngCheck]) {
            lat1 += 0.0005;
            lng1 += 0.0005;
            latLngCheck = lat1 + "," + lng1;
            if (!hmap[latLngCheck]) {
              marker.setPosition(new google.maps.LatLng(lat1, lng1));
              hmap[latLngCheck] = 1;
              break;
            }
          }
        }
        else {
          hmap[latLngCheck] = 1;
        }
        markerClusterer.addMarker(marker);
      }

      else {
        console.log(location + ': Geocode was not successful for the following reason: ' + status);
      }
    });
  });


});