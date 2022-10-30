var bookmarkBtns = document.getElementsByClassName("event-bookmark");

for (var i = 0; i < bookmarkBtns.length; i++) {
  bookmarkBtns[i].addEventListener("click", function () {
    var eventId = this.dataset.event;
    var action = this.dataset.action;
    console.log("eventId:", eventId, "action:", action);
    console.log("USER:", user);
    if (user === "AnonymousUser") {
      console.log("not logged in");
    } else {
      bookmarkUserEvent(eventId, action);
    }
  });
}

function bookmarkUserEvent(eventId, action) {
  console.log("User is authenticated, sending data");
  var url = "/bookmark_event/";
  console.log("URL:",url)
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      'eventId': eventId,
      'action': action,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      location.reload();
      console.log("data:", data);
      
    });
}
