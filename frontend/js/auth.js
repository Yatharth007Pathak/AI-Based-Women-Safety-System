// AUTHENTICATION MODULE


// REGISTER 
function register() {

    const full_name = document.getElementById("regName")?.value;
    const email = document.getElementById("regEmail")?.value;
    const password = document.getElementById("regPassword")?.value;
    const phone = document.getElementById("regPhone")?.value;

    if (!full_name || !email || !password) {
        showNotification("Please fill all required fields", "danger");
        return;
    }

    fetch(`${API_BASE}/auth/register`, { 
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            full_name,
            email,
            password,
            phone
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.message === "User registered successfully") {
            showNotification("Registration Successful! Please login.", "success");
        } else {
            showNotification(data.message || "Registration failed", "danger");
        }
    })
    .catch(() => {
        showNotification("Server error during registration", "danger");
    });
}


// LOGIN
function login() {

    const email = document.getElementById("loginEmail")?.value;
    const password = document.getElementById("loginPassword")?.value;

    if (!email || !password) {
        showNotification("Please enter email and password", "danger");
        return;
    }

    fetch(`${API_BASE}/auth/login`, {   
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email,
            password
        })
    })
    .then(res => res.json())
    .then(data => {

        if (data.token) {

            localStorage.setItem("token", data.token);

            showNotification("Login Successful!", "success");

            setTimeout(() => {
                window.location.href = "dashboard.html";
            }, 1000);

        } else {
            showNotification(data.message || "Login failed", "danger");
        }

    })
    .catch(() => {
        showNotification("Server error during login", "danger");
    });
}


// AUTO-REDIRECT
document.addEventListener("DOMContentLoaded", () => {

    if (window.location.pathname.includes("index.html") && getToken()) {
        window.location.href = "dashboard.html";
    }

});
