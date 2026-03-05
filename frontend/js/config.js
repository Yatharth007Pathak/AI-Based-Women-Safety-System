// CONFIGURATION FILE

// Backend Base URL
const API_BASE = "http://127.0.0.1:5000/api";

// Get JWT token from localStorage
function getToken() {
    return localStorage.getItem("token");
}

// Common headers for authenticated requests
function getAuthHeaders(isJSON = true) {
    const headers = {
        "Authorization": "Bearer " + getToken()
    };

    if (isJSON) {
        headers["Content-Type"] = "application/json";
    }

    return headers;
}

// Redirect to login if token not present
function requireAuth() {
    if (!getToken()) {
        window.location.href = "index.html";
    }
}

// Logout function (used globally)
function logout() {
    localStorage.removeItem("token");
    window.location.href = "index.html";
}

// Global Notification Helper
function showNotification(message, type = "info") {
    const notification = document.getElementById("notification");
    if (!notification) return;

    notification.textContent = message;
    notification.className = "notification show " + type;

    setTimeout(() => {
        notification.classList.remove("show");
    }, 4000);
}