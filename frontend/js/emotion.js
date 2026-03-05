// EMOTION MONITORING MODULE

let emotionInterval = null;

document.addEventListener("DOMContentLoaded", () => {
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");

    if (!video || !canvas) return;

    startCamera(video);
});


// START CAMERA 
function startCamera(videoElement) {

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            videoElement.srcObject = stream;

            // Start emotion detection loop
            emotionInterval = setInterval(() => {
                captureAndSendFrame(videoElement);
            }, 4000);

        })
        .catch(() => {
            showNotification("Camera access denied", "danger");
        });
}


// CAPTURE FRAME 
function captureAndSendFrame(videoElement) {

    const canvas = document.getElementById("canvas");
    const emotionResult = document.getElementById("emotionResult");

    if (!canvas || !emotionResult) return;

    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(videoElement, 0, 0);

    canvas.toBlob(blob => {

        const formData = new FormData();
        formData.append("image", blob);

        // Attach location for possible auto alert logging
        navigator.geolocation.getCurrentPosition(position => {

            formData.append("latitude", position.coords.latitude);
            formData.append("longitude", position.coords.longitude);

            sendEmotionData(formData);

        }, () => {
            sendEmotionData(formData);
        });

    }, "image/jpeg");
}


// SEND TO BACKEND 
function sendEmotionData(formData) {

    fetch(`${API_BASE}/emotion/detect`, {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + getToken()
        },
        body: formData
    })
    .then(res => res.json())
    .then(data => {

        const emotionResult = document.getElementById("emotionResult");

        if (data.emotion) {
            emotionResult.textContent = "Emotion: " + data.emotion;
        }

        if (data.auto_alert) {
            showNotification("⚠ Continuous Fear Detected! Auto Alert Triggered", "danger");

            // Also trigger backend alert system
            triggerAutoAlert("EMOTION_AUTO");
        }

    })
    .catch(() => {
        console.error("Emotion detection error");
    });
}


// AUTO ALERT TRIGGER 
function triggerAutoAlert(triggerType) {

    navigator.geolocation.getCurrentPosition(position => {

        fetch(`${API_BASE}/alerts/auto-alert`, {
            method: "POST",
            headers: getAuthHeaders(true),
            body: JSON.stringify({
                latitude: position.coords.latitude,
                longitude: position.coords.longitude,
                trigger_type: triggerType
            })
        });

    });
}