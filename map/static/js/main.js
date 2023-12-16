function addMarkerToGroup(group, coordinate, name, location, website, logo, contact, program) {
    var icon = new H.map.Icon('static/img/location.svg');
    var marker = new H.map.Marker(coordinate, { icon: icon });
    console.log(marker);
    // Create the HTML content for the marker
    var html = `<div style="display: flex; align-items: center;">
                    <img class="logo"src="${logo}" alt="${name} logo" style="margin-right: 10px" />
                    <div>
                    <a class="uni-title-link" href="${website}" target="_blank"><h2 class="uni-title">${name}</h2></a>
                    <p>${location}</p>
                    <p>Contact: ${contact}</p>
                    <p>Program: ${program}</p>
                    </div>
                </div>`;
    marker.setData(html);
    group.addObject(marker);
}

function addInfoBubble(map) {
    var group = new H.map.Group();
    var bubble = null;

    // Fetch the marker data from the server
    fetch('/api/markers')
        .then(response => response.text())  // Get the response as text
        .then(text => JSON.parse(text))  // Parse the text as JSON
        .then(markers => {
            console.log(markers);
            markers.forEach(marker => {
                var fields = marker.fields;
                console.log(fields);
                var name = fields.name;
                var location = fields.location;
                var website = fields.website;
                var logo = fields.logo;
                var contact = fields.contact;
                var program = fields.program;
                addMarkerToGroup(group, { lat: fields.lat, lng: fields.lng }, name, location, website, logo, contact, program);
            });
        });

    map.addObject(group);

    group.addEventListener('tap', function (evt) {

        if (bubble != null) {
            ui.removeBubble(bubble);
        }

        bubble = new H.ui.InfoBubble(evt.target.getGeometry(), {
            content: evt.target.getData()
        });
        ui.addBubble(bubble);

        var bubbleElement = bubble.getElement();

        var oldContentDiv = bubbleElement.querySelector('.H_ib_body');

        var newContentDiv = document.createElement('div');
        newContentDiv.innerHTML = oldContentDiv.innerHTML;
        newContentDiv.className = 'custom-bubble';
        oldContentDiv.parentNode.replaceChild(newContentDiv, oldContentDiv);

        var closeButtonDiv = newContentDiv.querySelector('.H_ib_close');

        var newCloseButton = document.createElement('button');
        newCloseButton.className = 'custom-bubble-close';
        newCloseButton.innerHTML = '<i class="fa fa-times"></i>';

        closeButtonDiv.parentNode.replaceChild(newCloseButton, closeButtonDiv);

        newCloseButton.addEventListener('click', function () {
            newContentDiv.classList.add('custom-bubble-closing');
            setTimeout(function () {
                ui.removeBubble(bubble);
            }, 300);
        });
    }, false);
}

var platform = new H.service.Platform({
    apikey: 'szrQPzoAGEM6OAnlea5YEQa8LkILYDP3QBv--ehKuKM'
});

var defaultLayers = platform.createDefaultLayers();

var map = new H.Map(
    document.getElementById('map'),
    defaultLayers.vector.normal.map,
    {
        zoom: 2.5,
        center: { lat: 20, lng: 0 }
    });

const ui = H.ui.UI.createDefault(map, defaultLayers);

var behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));

window.addEventListener('resize', () => map.getViewPort().resize());

addInfoBubble(map);
