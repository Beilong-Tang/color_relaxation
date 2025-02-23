document.addEventListener("DOMContentLoaded", function () {
    // Update the form to submit prompt audio to server
    document.querySelector("form").addEventListener("submit", async function(event) {
        event.preventDefault();
        let formData = new FormData(this);
        const backendServer = JSON.parse(document.getElementById("backend-path").textContent); // Get backend_path from HTML

        let response = await fetch(`${backendServer}/prompt_upload`, {
            method: "POST",
            body: formData
        });

        let result = await response.json();
        let messageElement = document.getElementById("upload-message");
        let currentTime = new Date().toLocaleString(); // Get current time as a string

        messageElement.textContent = `${result.message} (Uploaded at: ${currentTime})`;
        messageElement.style.color = result.success ? "green" : "red";
    });

    function getRandomColor(color) {
        console.log("Random Color get color: ", color);

        // Define a dictionary of specific colors
        const colorDict = {
            'red': '#FF0000', 'green': '#00FF00', 'blue': '#0000FF',
            'yellow': '#FFFF00', 'orange': '#FFA500', 'purple': '#800080',
            'pink': '#FFC0CB', 'brown': '#A52A2A', 'cyan': '#00FFFF', 'magenta': '#FF00FF'
        };

        // Convert the input color to lowercase
        const colorLowerCase = color.toLowerCase();
        
        // Check if the color is in the dictionary
        if (colorDict[colorLowerCase]) {
            return colorDict[colorLowerCase];
        } else {
            // If not found, return a random pink color
            const pinkShades = ['#FF69B4', '#FF1493', '#FFB6C1', '#FFC0CB'];
            return pinkShades[Math.floor(Math.random() * pinkShades.length)];
        }
    }

    async function generateResponse() {
        const chatBox = document.getElementById("chat-box");
        const userInput = document.getElementById("user-input");
        const prompt = userInput.value || "Give me a color therapy";
        chatBox.innerHTML += `<div class='chat-message'><b>You:</b> ${prompt}</div>`;
        userInput.value = "";
        
        try {
            const response = await fetch('/talk', {
                method: 'POST',
                body: new URLSearchParams({'prompt': prompt}),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            if (data.response) {
                const newColor = getRandomColor(data.color);
                document.body.style.backgroundColor = newColor;
                chatBox.innerHTML += `<div class='chat-message'><b>ChatGPT:</b> ${data.response}</div>`;
                insertAudioPlayer(data.response);
            } else {
                chatBox.innerHTML += `<div class='chat-message'><b>Error:</b> ${data.error}</div>`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        } catch (error) {
            console.error("Error fetching response:", error);
            chatBox.innerHTML += `<div class='chat-message'><b>Error:</b> Unable to fetch response.</div>`;
        }
    }

    async function insertAudioPlayer(responseText) {
        const chatBox = document.getElementById("chat-box");
        const backendServer = JSON.parse(document.getElementById("backend-path").textContent); // Get backend_path from HTML
        console.log("backend server: ", backendServer);

        try {
            const response = await fetch(`${backendServer}/wav?text=${encodeURIComponent(responseText)}`);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const audioBlob = await response.blob();
            const audioUrl = URL.createObjectURL(audioBlob);

            const audioElement = document.createElement("audio");
            audioElement.controls = true;
            audioElement.src = audioUrl;

            const audioWrapper = document.createElement("div");
            audioWrapper.innerHTML = `<b>Audio output:</b>`;
            audioWrapper.appendChild(audioElement);
            chatBox.appendChild(audioWrapper);
        } catch (error) {
            console.error("Error fetching audio:", error);
            chatBox.innerHTML += `<div class='chat-message'><b>Error:</b> Failed to load audio.</div>`;
        }
    }

    // Attach event listener for button click
    document.getElementById("generate-response-btn").addEventListener("click", generateResponse);
});
