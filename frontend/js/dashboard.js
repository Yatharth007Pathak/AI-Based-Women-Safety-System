// DASHBOARD CONTROLLER

document.addEventListener("DOMContentLoaded", () => {

    requireAuth();

    initLoader();
    initClock();
    initTheme();
    loadAlertHistory();
});


// LOADER 
function initLoader() {
    const loader = document.getElementById("loader");

    if (!loader) return;

    window.addEventListener("load", () => {
        loader.style.opacity = "0";
        setTimeout(() => loader.style.display = "none", 500);
    });
}


// CLOCK 
function initClock() {
    const clock = document.getElementById("liveClock");

    if (!clock) return;

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


// ALERT HISTORY (LOCAL ONLY)
function loadAlertHistory() {

    const list = document.getElementById("alertHistory");
    if (!list) return;

    list.innerHTML = "<li>No alerts yet</li>";
}


// ADD ALERT (REAL-TIME)
function addAlert(message) {

    const list = document.getElementById("alertHistory");
    if (!list) return;

    // remove placeholder
    if (list.innerHTML.includes("No alerts yet")) {
        list.innerHTML = "";
    }

    const li = document.createElement("li");

    li.textContent = `${new Date().toLocaleTimeString()} | ${message}`;

    // latest on top
    list.prepend(li);

    // limit to 10 alerts
    if (list.children.length > 10) {
        list.removeChild(list.lastChild);
    }
}


// SOS TRIGGER (SAFE DEMO)
function triggerSOS() {

    console.log("SOS triggered");

    showNotification("🚨 SOS Triggered!", "danger");

    addAlert("🚨 Manual SOS triggered!");

    const status = document.getElementById("sosStatus");

    if (status) {
        status.textContent = "Alert Sent";
        status.classList.remove("safe");
        status.classList.add("danger");
    }
}
