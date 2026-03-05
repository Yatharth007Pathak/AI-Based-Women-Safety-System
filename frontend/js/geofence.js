// GEOFENCE MONITORING MODULE

let geofenceInterval = null;


// INITIALIZE GEOFENCE
document.addEventListener("DOMContentLoaded", () => {

    const geoStatus = document.getElementById("geoStatus");
    if (!geoStatus) return;

    startGeoMonitoring();
});


// START LOCATION MONITORING 
function startGeoMonitoring() {

    if (!navigator.geolocation) {
        showNotification("Geolocation not supported", "danger");
        return;
    }

    // Check every 10 seconds
    geofenceInterval = setInterval(() => {

        navigator.geolocation.getCurrentPosition(position => {

            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            checkGeoFence(latitude, longitude);

        }, () => {
            showNotification("Location access denied", "danger");
        });

    }, 10000);
}


// CALL BACKEND
function checkGeoFence(latitude, longitude) {

    fetch(`${API_BASE}/geofence/check`, {
        method: "POST",
        headers: getAuthHeaders(true),
        body: JSON.stringify({
            latitude,
            longitude
        })
    })
    .then(res => res.json())
    .then(data => {

        const geoStatus = document.getElementById("geoStatus");
        if (!geoStatus) return;

        geoStatus.textContent = data.status;

        if (data.status === "HIGH_RISK_ZONE") {
            geoStatus.classList.remove("safe");
            geoStatus.classList.add("danger");

            showNotification("⚠ High Risk Area Detected!", "danger");

            triggerAutoAlert("GEOFENCE_AUTO");

        } else {
            geoStatus.classList.remove("danger");
            geoStatus.classList.add("safe");
        }

    })
    .catch(() => {
        console.error("Geofence check failed");
    });
}