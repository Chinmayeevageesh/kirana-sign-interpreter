
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

/* Shopkeeper Kannada Speech to English */


const replyTranslations = {
    // Grocery items
    "ಅಕ್ಕಿ": "Rice",
    "ಹಾಲು": "Milk",
    "ಸಕ್ಕರೆ": "Sugar",
    "ಅಂಗಡಿ": "Shop",
    "ನೀರು": "Water",
    "ಉಪ್ಪು": "Salt",
    "ಎಣ್ಣೆ": "Oil",
    "ಬೇಳೆ": "Dal",
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
    "ಇಪ್ಪತ್ತು ರೂಪಾಯಿ": "Twenty rupees",
    "ಹತ್ತು ರೂಪಾಯಿ": "Ten rupees",
    "ಐವತ್ತು ರೂಪಾಯಿ": "Fifty rupees",
    "ನೂರು ರೂಪಾಯಿ": "One hundred rupees",
    "ಇಲ್ಲ": "No",
    "ಹೌದು": "Yes",
    "ನಾಳೆ ಬನ್ನಿ": "Come tomorrow",
    "ಸ್ಟಾಕ್ ಇಲ್ಲ": "Out of stock"
};

/* Translate Kannada Text */

function translateKannada(text) {
    const cleaned = text.trim().replace(/[.,!?।]/g, "");

    document.getElementById("spokenKannada").textContent = text;

    const translation = replyTranslations[cleaned];

    document.getElementById("translatedEnglish").textContent =
        translation || "Translation not available for this phrase.";
}

/* Translate Typed Kannada */

document.getElementById("translateButton")
    .addEventListener("click", () => {
        const text = document.getElementById("kannadaInput").value;

        if (!text.trim()) {
            alert("Please enter Kannada text.");
            return;
        }

        translateKannada(text);
    });

/* Kannada Speech Recognition */

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

    listenButton.addEventListener("click", () => {
        listeningStatus.textContent = "Listening to Kannada...";
        recognition.start();
    });

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
        if (listeningStatus.textContent === "Listening to Kannada...") {
            listeningStatus.textContent = "Listening stopped.";
        }
    };
} else {
    listenButton.disabled = true;
    listeningStatus.textContent =
        "Speech recognition is not supported in this browser.";
}
