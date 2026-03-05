// DASHBOARD CONTROLLER

document.addEventListener("DOMContentLoaded", () => {

    // Protect Route
    requireAuth();

    initLoader();
    initClock();
    initTheme();
    loadAlertHistory();
});


// LOADER 
function initLoader() {
    const loader = document.getElementById("loader");

    window.addEventListener("load", () => {
        loader.style.opacity = "0";
        setTimeout(() => loader.style.display = "none", 500);
    });
}


// CLOCK 
function initClock() {
    const clock = document.getElementById("liveClock");

    function updateClock() {
        clock.textContent = new Date().toLocaleString();
    }

    setInterval(updateClock, 1000);
    updateClock();
}


// DARK MODE 
function initTheme() {
    const toggleBtn = document.getElementById("themeToggle");

    if (!toggleBtn) return;

    // Apply saved theme
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark");
        toggleBtn.textContent = "☀ Light Mode";
    }

    toggleBtn.addEventListener("click", () => {
        document.body.classList.toggle("dark");

        if (document.body.classList.contains("dark")) {
            toggleBtn.textContent = "☀ Light Mode";
            localStorage.setItem("theme", "dark");
        } else {
            toggleBtn.textContent = "🌙 Dark Mode";
            localStorage.setItem("theme", "light");
        }
    });
}


// ALERT HISTORY 
function loadAlertHistory() {

    fetch(`${API_BASE}/alerts/history`, {
        headers: getAuthHeaders(false)
    })
    .then(res => res.json())
    .then(data => {

        const list = document.getElementById("alertHistory");
        if (!list) return;

        list.innerHTML = "";

        if (!data.alerts || data.alerts.length === 0) {
            list.innerHTML = "<li>No alerts yet</li>";
            return;
        }

        data.alerts.forEach(alert => {
            const li = document.createElement("li");
            li.textContent = `${alert.alert_type} | ${alert.created_at}`;
            list.appendChild(li);
        });

    })
    .catch(() => {
        showNotification("Failed to load alert history", "danger");
    });
}


// SOS TRIGGER 
function triggerSOS() {

    navigator.geolocation.getCurrentPosition(position => {

        fetch(`${API_BASE}/alerts/sos`, {
            method: "POST",
            headers: getAuthHeaders(true),
            body: JSON.stringify({
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            })
        })
        .then(res => res.json())
        .then(data => {

            const status = document.getElementById("sosStatus");

            status.textContent = "Alert Sent";
            status.classList.remove("safe");
            status.classList.add("danger");

            showNotification("🚨 SOS Alert Sent!", "danger");

            loadAlertHistory();

        })
        .catch(() => {
            showNotification("SOS Failed", "danger");
        });

    }, () => {
        showNotification("Location access denied", "danger");
    });
}