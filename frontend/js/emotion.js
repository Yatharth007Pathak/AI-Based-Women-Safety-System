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

    // 🔥 CHANGE: send base64 instead of blob
    const imageData = canvas.toDataURL("image/jpeg");

    sendEmotionData(imageData);
}


// SEND TO BACKEND 
function sendEmotionData(imageData) {

    fetch(`${API_BASE}/emotion/predict`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + getToken()
        },
        body: JSON.stringify({
            image: imageData
        })
    })
    .then(res => res.json())
    .then(data => {

        const emotionResult = document.getElementById("emotionResult");

        if (data.emotion) {
            emotionResult.textContent = "Emotion: " + data.emotion;
        }

        if (data.auto_alert) {
            showNotification("⚠ Continuous Fear Detected! Auto Alert Triggered", "danger");
            addAlert("😨 Fear detected");
        }

    })
    .catch(() => {
        console.error("Emotion detection error");
    });
}
