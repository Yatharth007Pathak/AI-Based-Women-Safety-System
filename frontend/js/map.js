function initMap() {

    // Kanpur coordinates
    const lat = 26.4499;
    const lng = 80.3319;

    const map = L.map('map').setView([lat, lng], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
    }).addTo(map);

    L.marker([lat, lng])
        .addTo(map)
        .bindPopup("📍 You are here")
        .openPopup();
}

// load map
window.onload = initMap;
