// Audio autoplay after it is ended
const audio = document.getElementById("background-music");
audio.volume = 0.3 // start volume to be 0.3
audio.addEventListener("ended", function () {
    this.currentTime = 0;  // Reset to start
    this.play();           // Play again
});

// Customize bar
// Function to open the modal
function openCustomize() {
    document.getElementById("modal-customize").style.display = "block";
    document.getElementById("overlay-customize").style.display = "block";
}

// Function to close the modal
function closeCustomize() {
    document.getElementById("modal-customize").style.display = "none";
    document.getElementById("overlay-customize").style.display = "none";
}

function closeContent(event){
    const modal = event.target.closest(".section");
    if (modal) {
      const modalContent = modal.querySelector(".section-modal-content");
      if (modalContent) {
        if (modalContent.style.display != 'none'){
            modalContent.style.display = "none";
            // Toggle text to be DISPLAY
            event.target.innerText="DISPLAY"
        }
        else {
            modalContent.style.display = "block"; 
            event.target.innerText="HIDE"
        }
      }

    }
}


function closeModal(event) {
    // Find the closest parent modal and then hide its content
    const modal = event.target.closest(".section");
    if (modal) {
      const modalContent = modal.querySelector(".section-modal");
      if (modalContent) {
        modalContent.style.display = "none";
        let audio = modal.querySelector(".prompt-audio")
        audio.pause();
        audio.currentTime = 0;
      }
    }
  }

// For each modal instance
document.addEventListener("click", function(event) {
    // Open the closest modal when clicking a button
    if (event.target.classList.contains("section-open-modal")) {
        let modal = event.target.closest(".section").querySelector(".section-modal");
        if (modal) modal.style.display = "flex";
        // play the audio
        let audio = event.target.closest(".section").querySelector(".prompt-audio");
        audio.play();
    }

});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function typeText(element, text) {
    const words = text.split(' '); // Split the text into words
    let index = 0;
    
    // Use a while loop to iterate through the words
    while (index < words.length) {
        // Append one word at a time to the element
        element.innerHTML += words[index] + ' ';
        
        // Wait for 500ms before adding the next word (adjust speed as needed)
        await sleep(100);
        
        // Move to the next word
        index++;
        element.scrollIntoView({ behavior: "smooth", block: "end" });
    }
}

document.addEventListener("DOMContentLoaded", function () {
    // Update the form to submit prompt audio to server
    document.querySelector("form").addEventListener("submit", async function (event) {
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
        document.getElementById("generate-response-btn").disabled = true; 
        const chatBox = document.getElementById("chat-box");
        const userInput = document.getElementById("user-input");
        const prompt = userInput.value || "Give me a color therapy";
        chatBox.innerHTML += `<div class='chat-message'><b>You:</b> ${prompt}</div>`;
        userInput.value = "";

        try {
            const response = await fetch('/talk', {
                method: 'POST',
                body: new URLSearchParams({ 'prompt': prompt }),
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            if (data.response) {
                const newColor = getRandomColor(data.color);
                document.body.style.backgroundColor = newColor;
                chatBox.innerHTML += `<div class='chat-message'><b>Agent:</b></div>`;
                element = chatBox.lastElementChild;
                console.log(element)
                // Add text to it
                console.log(data.response)
                // typeText(element,data.response)
                // insertAudioPlayer(data.response, data.color);
                await Promise.all([typeText(element,data.response), insertAudioPlayer(data.response, data.color)]);
                console.log("Done")
                console.log(element)
                element.innerHTML = data.response
                
            } else {
                chatBox.innerHTML += `<div class='chat-message'><b>Error:</b> ${data.error}</div>`;
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        } catch (error) {
            console.error("Error fetching response:", error);
            chatBox.innerHTML += `<div class='chat-message'><b>Error:</b> Unable to fetch response.</div>`;
        }
        document.getElementById("generate-response-btn").disabled = false;
    }

    async function insertAudioPlayer(responseText, color) {
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
            

            // Whether to add audio or not
            // const audioWrapper = document.createElement("div");
            // audioWrapper.innerHTML = `<b>Audio output:</b>`;
            // audioWrapper.appendChild(audioElement);
            // chatBox.appendChild(audioWrapper);
            
            // Also try to add the modal to it
            console.log(color.toLowerCase())
            color = color.toLowerCase()
            let cur_col = ""
            if (color.includes("red")){
                cur_col="red"
            }
            else if  (color.includes("green")){
                cur_col="green"
            }
            else if  (color.includes("yellow")){
                cur_col="yellow"
            }
            else if  (color.includes("purple")){
                cur_col="purple"
            }
            else if  (color.includes("orange")){
                cur_col="orange"
            }
            else if  (color.includes("blue")){
                cur_col="blue"
            }
            console.log("Current color", cur_col)

            const newHTML = `
                <div class="section">
                    <button class="section-open-modal">RELAX</button>
                    <div class="section-modal back-${cur_col}">
                    <div class="close section-close-modal">
                        <span style='margin-right:30px' onclick="closeContent(event)" class='section-hide'>HIDE</span>
                        <span onclick="closeModal(event)">X</span>
                    </div>
                        <div class="section-modal-content">
                            <p>${responseText}</p>
                            <audio controls class="prompt-audio">
                                <source src="${audioUrl}" type="audio/mpeg">
                                Your browser does not support the audio element.
                            </audio>
                        </div>
                    </div>
                </div>
            `;
            chatBox.innerHTML += newHTML; // Append the HTML
            const lastElement = chatBox.lastElementChild;
            // Scroll to the new element
            if (lastElement) {
                lastElement.scrollIntoView({ behavior: "smooth", block: "end" });
            }



        } catch (error) {
            console.error("Error fetching audio:", error);
            chatBox.innerHTML += `<div class='chat-message'><b>Error:</b> Failed to load audio.</div>`;
        }
    }

    // Attach event listener for button click
    document.getElementById("generate-response-btn").addEventListener("click", generateResponse);
});
