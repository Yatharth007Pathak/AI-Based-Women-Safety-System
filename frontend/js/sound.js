// SOUND MONITORING MODULE

let mediaRecorder = null;
let audioChunks = [];
let isMonitoring = false;
let streamRef = null;


// START / STOP AUDIO MONITORING
function startAudioMonitoring() {

    const btn = document.getElementById("audioBtn");

    // 🔥 TOGGLE LOGIC (FIXED)
    if (isMonitoring) {
        isMonitoring = false;
        btn.classList.remove("active");
        btn.innerText = "Start Audio Monitoring";
        document.getElementById("soundResult").innerText = "Audio monitoring stopped";

        // stop mic
        if (streamRef) {
            streamRef.getTracks().forEach(track => track.stop());
        }

        showNotification("🛑 Monitoring stopped", "info");
        return;
    }

    // START
    isMonitoring = true;
    btn.classList.add("active");
    btn.innerText = "Monitoring...";
    document.getElementById("soundResult").innerText = "Listening...";

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {

            streamRef = stream;

            showNotification("🎤 Live audio monitoring started", "success");

            const recordLoop = () => {

                if (!isMonitoring) return;

                mediaRecorder = new MediaRecorder(stream, {
                    mimeType: "audio/webm"
                });

                audioChunks = [];

                mediaRecorder.start();

                mediaRecorder.ondataavailable = event => {
                    if (event.data.size > 0) {
                        audioChunks.push(event.data);
                    }
                };

                // record 3 sec
                setTimeout(() => {
                    if (mediaRecorder.state !== "inactive") {
                        mediaRecorder.stop();
                    }
                }, 3000);

                mediaRecorder.onstop = () => {

                    const audioBlob = new Blob(audioChunks, {
                        type: "audio/webm"
                    });

                    sendAudioToBackend(audioBlob);

                    // loop continue
                    setTimeout(recordLoop, 500);
                };
            };

            recordLoop();

        })
        .catch(() => {
            showNotification("Microphone access denied", "danger");
        });
}


// SEND AUDIO TO BACKEND
function sendAudioToBackend(audioBlob) {

    const formData = new FormData();
    formData.append("audio", audioBlob, "recording.webm");

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

        // 🔥 FIXED DISPLAY
        if (data.sound) {
            soundResult.innerText = "Sound: " + data.sound;
        } else {
            soundResult.innerText = "No sound detected";
        }

        if (data.auto_alert) {
            showNotification("⚠ Distress Sound Detected! Auto Alert Triggered", "danger");
            addAlert("🚨 Distress sound detected");
        }

    })
    .catch(() => {
        showNotification("Sound detection failed", "danger");
    });
}
