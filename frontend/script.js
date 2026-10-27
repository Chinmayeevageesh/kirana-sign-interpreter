
const groceryItems = {
    rice: "ಅಕ್ಕಿ",
    milk: "ಹಾಲು",
    sugar: "ಸಕ್ಕರೆ"
};

function showResult(label) {
    const englishResult = document.getElementById("englishResult");
    const kannadaResult = document.getElementById("kannadaResult");

    if (groceryItems[label]) {
        englishResult.textContent = label;
        kannadaResult.textContent = groceryItems[label];
    } else {
        englishResult.textContent = "Sign not recognized";
        kannadaResult.textContent = "-";
    }
}

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

document.getElementById("startCamera").addEventListener("click", async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
        });

        document.getElementById("webcam").srcObject = stream;
    } catch (error) {
        alert("Unable to access camera. Please check permissions.");
        console.error(error);
    }
});
