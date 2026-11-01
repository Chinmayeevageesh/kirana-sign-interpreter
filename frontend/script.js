
/* =========================================
   KIRANA SIGN INTERPRETER - FRONTEND
   Member 3: Frontend Development
========================================= */


/* 1. Grocery Items and Kannada Names */

const groceryItems = {
    rice: "ಅಕ್ಕಿ",
    milk: "ಹಾಲು",
    sugar: "ಸಕ್ಕರೆ",
    salt: "ಉಪ್ಪು",
    oil: "ಎಣ್ಣೆ",
    dal: "ಬೇಳೆ",
    wheat: "ಗೋಧಿ",
    tea: "ಚಹಾ",
    coffee: "ಕಾಫಿ",
    biscuit: "ಬಿಸ್ಕತ್ತು"
};


/* 2. Display Recognition Result */

function showResult(label) {
    const englishResult = document.getElementById("englishResult");
    const kannadaResult = document.getElementById("kannadaResult");
    const status = document.getElementById("recognitionStatus");

    const item = typeof label === "string"
        ? label.trim().toLowerCase()
        : "";

    if (Object.prototype.hasOwnProperty.call(groceryItems, item)) {
        englishResult.textContent =
            item.charAt(0).toUpperCase() + item.slice(1);

        kannadaResult.textContent = groceryItems[item];

        status.textContent = "Sign recognized successfully!";
        status.style.color = "green";
    } else {
        englishResult.textContent = "Sign not recognized";
        kannadaResult.textContent = "-";

        status.textContent = "Unknown sign. Please try again.";
        status.style.color = "red";
    }
}


/* 3. Simulate Backend Recognition */

function simulateBackendResponse(label) {
    const status = document.getElementById("recognitionStatus");

    status.textContent = "Recognizing sign...";
    status.style.color = "#175cd3";

    setTimeout(() => {
        const response = {
            label: label,
            recognized: label !== "unknown",
            distance: label === "unknown" ? null : 0.12,
            status: label === "unknown"
                ? "unknown"
                : "recognized"
        };

        if (response.recognized) {
            showResult(response.label);
        } else {
            showResult(null);
        }
    }, 1000);
}


/* 4. Kannada Text-to-Speech */

document.getElementById("speakButton")
    .addEventListener("click", () => {

        const text = document.getElementById("kannadaResult")
            .textContent.trim();

        if (text === "-" || !text) {
            alert("Please recognize a grocery item first.");
            return;
        }

        if (!("speechSynthesis" in window)) {
            alert("Text-to-speech is not supported in this browser.");
            return;
        }

        const speech = new SpeechSynthesisUtterance(text);

        speech.lang = "kn-IN";
        speech.rate = 0.85;

        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(speech);
    });


/* 5. Start Webcam */

let cameraStream = null;

document.getElementById("startCamera")
    .addEventListener("click", async () => {

        const status = document.getElementById("recognitionStatus");
        const webcam = document.getElementById("webcam");

        try {
            status.textContent = "Starting camera...";
            status.style.color = "#175cd3";

            if (!navigator.mediaDevices ||
                !navigator.mediaDevices.getUserMedia) {
                throw new Error("Camera API not supported.");
            }

            if (cameraStream) {
                cameraStream.getTracks().forEach(track => track.stop());
            }

            cameraStream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: false
            });

            webcam.srcObject = cameraStream;
            await webcam.play();

            status.textContent = "Camera ready. Waiting for sign...";
            status.style.color = "#175cd3";

        } catch (error) {
            status.textContent = "Camera access failed.";
            status.style.color = "red";

            alert("Unable to access camera. Please check permissions.");
            console.error("Camera error:", error);
        }
    });


/* 6. Kannada-to-English Translation Dictionary */

const replyTranslations = {

    // Grocery items
    "ಅಕ್ಕಿ": "Rice",
    "ಹಾಲು": "Milk",
    "ಸಕ್ಕರೆ": "Sugar",
    "ಉಪ್ಪು": "Salt",
    "ಎಣ್ಣೆ": "Oil",
    "ಬೇಳೆ": "Dal",
    "ಗೋಧಿ": "Wheat",
    "ಚಹಾ": "Tea",
    "ಕಾಫಿ": "Coffee",

    // Biscuit spelling variations
    "ಬಿಸ್ಕತ್ತು": "Biscuit",
    "ಬಿಸ್ಕಟ್ಟು": "Biscuit",
    "ಬಿಸ್ಕೆಟ್": "Biscuit",

    // Other useful words
    "ನೀರು": "Water",
    "ಅಂಗಡಿ": "Shop",
    "ತರಕಾರಿ": "Vegetables",

    // Greetings
    "ಹಲೋ": "Hello",
    "ನಮಸ್ಕಾರ": "Hello",
    "ಹೇಗಿದ್ದೀರಾ": "How are you?",
    "ಚೆನ್ನಾಗಿದ್ದೇನೆ": "I am fine",
    "ಸ್ವಾಗತ": "Welcome",
    "ಧನ್ಯವಾದ": "Thank you",
    "ದಯವಿಟ್ಟು": "Please",
    "ಕ್ಷಮಿಸಿ": "Sorry",
    "ಸರಿ": "Okay",

    // Shopkeeper conversations
    "ಎಷ್ಟು": "How much?",
    "ಎಷ್ಟು ಬೇಕು": "How much do you need?",
    "ಏನು ಬೇಕು": "What do you need?",
    "ಅಕ್ಕಿ ಬೇಕಾ": "Do you want rice?",
    "ಹಾಲು ಬೇಕಾ": "Do you want milk?",
    "ಸಕ್ಕರೆ ಬೇಕಾ": "Do you want sugar?",

    // Prices
    "ಹತ್ತು ರೂಪಾಯಿ": "Ten rupees",
    "ಇಪ್ಪತ್ತು ರೂಪಾಯಿ": "Twenty rupees",
    "ಐವತ್ತು ರೂಪಾಯಿ": "Fifty rupees",
    "ನೂರು ರೂಪಾಯಿ": "One hundred rupees",

    // Other responses
    "ಇಲ್ಲ": "No",
    "ಹೌದು": "Yes",
    "ನಾಳೆ ಬನ್ನಿ": "Come tomorrow",
    "ಸ್ಟಾಕ್ ಇಲ್ಲ": "Out of stock"
};


/* 7. Translate Kannada Text into English */

function translateKannada(text) {

    const cleaned = text
        .trim()
        .replace(/[.,!?।,，!?]/g, "")
        .replace(/\s+/g, " ");

    const spokenKannada = document.getElementById("spokenKannada");
    const translatedEnglish = document.getElementById("translatedEnglish");

    spokenKannada.textContent = text;

    const translation = replyTranslations[cleaned];

    if (translation) {
        translatedEnglish.textContent = translation;
        translatedEnglish.style.color = "#167a52";
    } else {
        translatedEnglish.textContent =
            "Translation not available for this phrase.";

        translatedEnglish.style.color = "#b45309";
    }
}


/* 8. Translate Manually Typed Kannada */

document.getElementById("translateButton")
    .addEventListener("click", () => {

        const text = document.getElementById("kannadaInput").value;

        if (!text.trim()) {
            alert("Please enter Kannada text.");
            return;
        }

        translateKannada(text);
    });


/* 9. Kannada Speech Recognition */

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

const listenButton = document.getElementById("listenButton");
const listeningStatus = document.getElementById("listeningStatus");

if (SpeechRecognition) {

    const recognition = new SpeechRecognition();

    recognition.lang = "kn-IN";
    recognition.continuous = false;
    recognition.interimResults = false;

    let isListening = false;

    listenButton.addEventListener("click", () => {

        if (isListening) {
            return;
        }

        try {
            recognition.start();
        } catch (error) {
            listeningStatus.textContent =
                "Unable to start listening. Please try again.";

            console.error("Speech recognition error:", error);
        }
    });

    recognition.onstart = () => {
        isListening = true;
        listenButton.disabled = true;
        listeningStatus.textContent = "Listening to Kannada...";
    };

    recognition.onresult = (event) => {

        const spokenText = event.results[0][0].transcript;

        listeningStatus.textContent = "Speech captured!";

        document.getElementById("kannadaInput").value = spokenText;

        translateKannada(spokenText);
    };

    recognition.onerror = (event) => {

        listeningStatus.textContent =
            "Speech recognition error: " + event.error;
    };

    recognition.onend = () => {

        isListening = false;
        listenButton.disabled = false;

        if (listeningStatus.textContent === "Listening to Kannada...") {
            listeningStatus.textContent = "Listening stopped.";
        }
    };

} else {

    listenButton.disabled = true;

    listeningStatus.textContent =
        "Speech recognition is not supported in this browser.";
}
