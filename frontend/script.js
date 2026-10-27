
/* Grocery Items and Kannada Names */

const groceryItems = {
    rice: "ಅಕ್ಕಿ",
    milk: "ಹಾಲು",
    sugar: "ಸಕ್ಕರೆ"
};

/* Display Recognition Result */

function showResult(label) {
    const englishResult = document.getElementById("englishResult");
    const kannadaResult = document.getElementById("kannadaResult");
    const status = document.getElementById("recognitionStatus");

    if (groceryItems[label]) {
        englishResult.textContent = label;
        kannadaResult.textContent = groceryItems[label];

        status.textContent = "Sign recognized successfully!";
        status.style.color = "green";
    } else {
        englishResult.textContent = "Sign not recognized";
        kannadaResult.textContent = "-";

        status.textContent = "Unknown sign. Please try again.";
        status.style.color = "red";
    }
}

/* Simulate Backend Recognition */

function simulateBackendResponse(label) {
    const status = document.getElementById("recognitionStatus");

    status.textContent = "Recognizing sign...";
    status.style.color = "#175cd3";

    setTimeout(() => {
        const response = {
            label: label,
            recognized: label !== "unknown",
            distance: label === "unknown" ? null : 0.12
        };

        if (response.recognized) {
            showResult(response.label);
        } else {
            showResult("unknown");
        }
    }, 1000);
}

/* Kannada Text-to-Speech */

document.getElementById("speakButton").addEventListener("click", () => {
    const text = document.getElementById("kannadaResult").textContent;

    if (text === "-") {
        alert("Please recognize a grocery item first.");
        return;
    }

    const speech = new SpeechSynthesisUtterance(text);

    speech.lang = "kn-IN";
    speech.rate = 0.85;

    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(speech);
});

/* Start Webcam */

document.getElementById("startCamera").addEventListener("click", async () => {
    const status = document.getElementById("recognitionStatus");

    try {
        status.textContent = "Starting camera...";

        const stream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
        });

        document.getElementById("webcam").srcObject = stream;

        status.textContent = "Camera ready. Waiting for sign...";
        status.style.color = "#175cd3";

    } catch (error) {
        status.textContent = "Camera access failed.";
        status.style.color = "red";

        alert("Unable to access camera. Please check permissions.");
        console.error(error);
    }
});
