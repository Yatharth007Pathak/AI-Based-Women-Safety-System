// GOOGLE MAP + CRIME HEATMAP MODULE

let map;
let heatmap;


// INITIALIZE MAP
document.addEventListener("DOMContentLoaded", () => {

    const mapElement = document.getElementById("map");
    if (!mapElement) return;

    initMap();
});


// INIT MAP 
function initMap() {

    if (!navigator.geolocation) {
        showNotification("Geolocation not supported", "danger");
        return;
    }

    navigator.geolocation.getCurrentPosition(position => {

        const userLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };

        map = new google.maps.Map(document.getElementById("map"), {
            zoom: 14,
            center: userLocation
        });

        // User marker
        new google.maps.Marker({
            position: userLocation,
            map: map,
            title: "Your Location"
        });

        loadCrimeHeatmap();

    }, () => {
        showNotification("Location access denied", "danger");
    });
}


// LOAD CRIME DATA 
function loadCrimeHeatmap() {

    fetch(`${API_BASE}/geofence/crime-data`, {
        headers: getAuthHeaders(false)
    })
    .then(res => res.json())
    .then(data => {

        if (!data.crime_data) return;

        const heatmapData = data.crime_data.map(point => {

            return {
                location: new google.maps.LatLng(
                    parseFloat(point.latitude),
                    parseFloat(point.longitude)
                ),
                weight: point.risk_score
            };
        });

        heatmap = new google.maps.visualization.HeatmapLayer({
            data: heatmapData,
            radius: 30
        });

        heatmap.setMap(map);

    })
    .catch(() => {
        console.error("Failed to load heatmap data");
    });
}