const btn1BikeLane = document.getElementById("btn1");
const btn2BikePark = document.getElementById("btn2");
const btn3BikeColl = document.getElementById("btn3");
const btn4RepIssue = document.getElementById("btn4");

/*
  BUTTON 1: Bike Lanes
*/

btn1BikeLane.addEventListener("click", function onClick() {
  btn1BikeLane.classList.remove("btn-secondary");
  btn1BikeLane.classList.add("btn-primary");
  btn2BikePark.classList.remove("btn-primary");
  btn3BikeColl.classList.remove("btn-primary");
  btn4RepIssue.classList.remove("btn-primary");
  btn2BikePark.classList.add("btn-secondary");
  btn3BikeColl.classList.add("btn-secondary");
  btn4RepIssue.classList.add("btn-secondary");

  const uluru = { lat: 40.7237, lng: -73.9898 };

  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 15,
    center: uluru,
  });

  const bikeLayer = new google.maps.BicyclingLayer();
  bikeLayer.setMap(map);
});

/*
  BUTTON 2: Bike Parking
*/

btn2BikePark.addEventListener("click", function onClick() {
  btn2BikePark.classList.remove("btn-secondary");
  btn2BikePark.classList.add("btn-primary");
  btn1BikeLane.classList.remove("btn-primary");
  btn3BikeColl.classList.remove("btn-primary");
  btn4RepIssue.classList.remove("btn-primary");
  btn1BikeLane.classList.add("btn-secondary");
  btn3BikeColl.classList.add("btn-secondary");
  btn4RepIssue.classList.add("btn-secondary");

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
  btn1BikeLane.classList.add("btn-secondary");
  btn2BikePark.classList.add("btn-secondary");
  btn4RepIssue.classList.add("btn-secondary");

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
      "<b>Crash Date:</b> " +  date + "<br>" + 
      "<b>Crash Time (military time):</b> " + time + "<br>" +
      "<b>Borough:</b> " + borough + "<br>" + 
      "<b>Zipcode:</b> " + zip + "<br>" +
      "<b>Cyclists Injured:</b> " +  numInjured + "<br>" +
      "<b>Cyclists Killed:</b> " +  numKilled + "<br>";
    infowindow.setContent(html);
    infowindow.setPosition(event.latLng);
    infowindow.setOptions({ pixelOffset: new google.maps.Size(0, -30) });
    infowindow.open(map);
  });
});

/*
  BUTTON 4: Reported Lane Issues
*/
// write code here
btn4RepIssue.addEventListener("click", function onClick() {
  btn4RepIssue.classList.remove("btn-secondary");
  btn4RepIssue.classList.add("btn-primary");
  btn3BikeColl.classList.remove("btn-secondary");
  btn1BikeLane.classList.remove("btn-primary");
  btn2BikePark.classList.remove("btn-primary");
  btn3BikeColl.classList.remove("btn-primary");
  btn1BikeLane.classList.add("btn-secondary");
  btn2BikePark.classList.add("btn-secondary");
  btn3BikeColl.classList.add("btn-secondary");

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

  let locations = [];
  for (let i = 0; i < issueObjsJson.length; i++) {
    console.log(issueObjsJson[i]);
    let t1 = {};
    t1['lat'] = parseFloat(issueObjsJson[i]['fields']['latitude']);
    t1['lng'] = parseFloat(issueObjsJson[i]['fields']['longitude']);
    locations.push(t1);
  }

  const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

  // Add some markers to the map.
  const markers = locations.map((position, i) => {
    console.log(position);
    const label = labels[i % labels.length];
    const marker = new google.maps.Marker({
      position,
      label,
    });

    // markers can only be keyboard focusable when they have click listeners
    // open info window when marker is clicked
    marker.addListener("click", () => {
      infoWindow.setContent(label);
      infoWindow.open(map, marker);
    });

    return marker;
  });

  // Add a marker clusterer to manage the markers.
  // new MarkerClusterer({ markers, map });

 });


/*
  INITIALIZE MAP
*/

function initMap() {
  const uluru = { lat: 40.7237, lng: -73.9898 };

  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 11,
    center: uluru,
  });

  const bikeLayer = new google.maps.BicyclingLayer();
  bikeLayer.setMap(map);
}
