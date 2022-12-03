const btn1 = document.getElementById("btn1");
const btn2 = document.getElementById("btn2");
const btn3 = document.getElementById("btn3");
const btn4 = document.getElementById("btn4");

/*
  BUTTON 1: Bike Lanes
*/

btn1.addEventListener("click", function onClick() {
  btn1.classList.remove("btn-secondary");
  btn1.classList.add("btn-primary");
  btn2.classList.remove("btn-primary");
  btn3.classList.remove("btn-primary");
  btn4.classList.remove("btn-primary");
  btn2.classList.add("btn-secondary");
  btn3.classList.add("btn-secondary");
  btn4.classList.add("btn-secondary");

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

btn2.addEventListener("click", function onClick() {
  btn2.classList.remove("btn-secondary");
  btn2.classList.add("btn-primary");
  btn1.classList.remove("btn-primary");
  btn3.classList.remove("btn-primary");
  btn4.classList.remove("btn-primary");
  btn1.classList.add("btn-secondary");
  btn3.classList.add("btn-secondary");
  btn4.classList.add("btn-secondary");

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

btn3.addEventListener("click", function onClick() {
  btn3.classList.remove("btn-secondary");
  btn3.classList.add("btn-primary");
  btn1.classList.remove("btn-primary");
  btn2.classList.remove("btn-primary");
  btn4.classList.remove("btn-primary");
  btn1.classList.add("btn-secondary");
  btn2.classList.add("btn-secondary");
  btn4.classList.add("btn-secondary");

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
btn4.addEventListener("click", function onClick() {
  btn4.classList.remove("btn-secondary");
  btn4.classList.add("btn-primary");
  btn3.classList.remove("btn-secondary");
  btn1.classList.remove("btn-primary");
  btn2.classList.remove("btn-primary");
  btn3.classList.remove("btn-primary");
  btn1.classList.add("btn-secondary");
  btn2.classList.add("btn-secondary");
  btn3.classList.add("btn-secondary");

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

  for (let i = 0; i < issueCoordinates.length; i++) {
    console.log(issueCoordinates[i]);
  }

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
