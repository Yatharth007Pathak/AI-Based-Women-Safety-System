// SOUND MONITORING MODULE

let mediaRecorder = null;
let audioChunks = [];


// START AUDIO MONITORING 
function startAudioMonitoring() {

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {

            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.start();
            showNotification("🎤 Audio monitoring started", "info");

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            // Stop recording after 3 seconds
            setTimeout(() => {
                if (mediaRecorder.state !== "inactive") {
                    mediaRecorder.stop();
                }
            }, 3000);

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
                sendAudioToBackend(audioBlob);
            };

        })
        .catch(() => {
            showNotification("Microphone access denied", "danger");
        });
}


// SEND AUDIO TO BACKEND
function sendAudioToBackend(audioBlob) {

    const formData = new FormData();
    formData.append("audio", audioBlob);

    fetch(`${API_BASE}/sound/detect`, {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + getToken()
        },
        body: formData
    })
    .then(res => res.json())
    .then(data => {

        const soundResult = document.getElementById("soundResult");

        if (data.sound_status) {
            soundResult.textContent = "Sound: " + data.sound_status;
        }

        if (data.auto_alert) {
            showNotification("⚠ Distress Sound Detected! Auto Alert Triggered", "danger");
            triggerAutoAlert("SOUND_AUTO");
        }

    })
    .catch(() => {
        showNotification("Sound detection failed", "danger");
    });
}