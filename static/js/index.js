const add_data = document.getElementById("add-data");
const add_pdf = document.getElementById("add-pdf");
const send = document.getElementById("send");
let chat = document.getElementById("chat-input");
const mic = document.getElementById("mic");

// Trigger file selection when clicking the "add-data" button
add_data.addEventListener("click", function () {
    add_pdf.click();
});

// Handle the event when a file is selected
add_pdf.addEventListener("change", function (event) {
    const file = event.target.files[0]; // Get the first selected file

    if (!file) {
        alert("No file chosen!"); // Notify user if no file is selected
        return;
    }

    const formData = new FormData();
    formData.append("file", file); // Append the file to FormData

    // Send file to the server via a POST request
    fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => console.log("Success:", data))
    .catch(error => console.error("Error:", error));

    load_doc(); // Reload document list after uploading
});

// Handle sending messages
send.addEventListener("click", async function(){
    const chatContainer = document.querySelector('.chat-container');

    const observer = new MutationObserver(() => {
        scrollToBottom();
    });
    
    observer.observe(chatContainer, {
        childList: true,
        subtree: true
    });

    const message = chat.value; 
    chat.value = null; // Clear input field after sending

    if (!message.trim()) return; // Prevent sending empty messages

    const file_items = document.querySelectorAll(".file-item");
    const file_name = [];

    // Collect the names of selected files
    file_items.forEach(file => {
        const checkbox = file.querySelector("input[type='checkbox']");
        if (checkbox.checked) {
            file_name.push(file.textContent);
        }
    });
    if (!file_name){
        alert("No file choose!")
        return
    }
    add_new_message(message);
    console.log(message);

    // Send message and selected file names to the server
    const response = await fetch("/user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "message": message, "file_name": file_name }),
    });

    const data = await response.json();
    add_new_respone(data);
    
    observer.observe(chatContainer, {
        childList: true,
        subtree: true
    });
});

// Load all previous messages from the server
async function load_message() {
    const response = await fetch("/load_all");
    const datas = await response.json();

    if (!datas) return;
    console.log(datas);

    const chatShow = document.querySelector(".chat-show");
    chatShow.innerHTML = ""; // Clear previous content

    datas.forEach((data) => {
        const messageuserDiv = document.createElement("div"); // User message
        const messageresponeDiv = document.createElement("div"); // AI model response

        messageuserDiv.classList.add("message-box", "user-message");
        messageresponeDiv.classList.add("bot-response");

        messageuserDiv.textContent = data.message;
        messageresponeDiv.textContent = data.response;

        chatShow.appendChild(messageuserDiv); // Add user message
        chatShow.appendChild(messageresponeDiv); // Add AI response
    });

    // Scroll to the bottom to show the latest message
    chatShow.scrollTop = chatShow.scrollHeight;
}

load_message(); // Load messages when the page loads

// Function to add a new user message to the chat
function add_new_message(message) {
    const chatShow = document.querySelector(".chat-show");

    const messageuserDiv = document.createElement("div");
    messageuserDiv.classList.add("message-box", "user-message");
    messageuserDiv.textContent = message;

    chatShow.appendChild(messageuserDiv);
}

// Function to add a new AI response to the chat
function add_new_respone(response) {
    const chatShow = document.querySelector(".chat-show");

    const messageresponeDiv = document.createElement("div");
    messageresponeDiv.classList.add("message-box", "bot-response");
    messageresponeDiv.textContent = response;

    chatShow.appendChild(messageresponeDiv);
}

// Load available documents from the server
async function load_doc() {
    const response = await fetch("http://localhost:8000/load_file");
    const datas = await response.json(); // Convert response to JSON
    if (!datas) return;
    const fileShowDiv = document.getElementById("file-show");
    fileShowDiv.innerHTML = ""; // Clear previous content

    datas.forEach(data => {
        const fileElement = document.createElement("div");
        fileElement.classList.add("file-item");

        // Create a checkbox
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.value = data;

        // Create a span for the file name
        const fileName = document.createElement("span");
        fileName.textContent = data;

        // Toggle checkbox selection when clicking on file-item
        fileElement.addEventListener("click", () => {
            checkbox.checked = !checkbox.checked;
        });

        // Append checkbox & file name to fileElement
        fileElement.appendChild(checkbox);
        fileElement.appendChild(fileName);
        fileShowDiv.appendChild(fileElement);
    });
}

// Load documents when the page is fully loaded
document.addEventListener("DOMContentLoaded", load_doc());

const delete_file = document.getElementById("delete-file")

delete_file.addEventListener("click", async function(){
    const file_name = [];
    const file_items = document.querySelectorAll(".file-item");
    // Collect the names of selected files
    file_items.forEach(file => {
        const checkbox = file.querySelector("input[type='checkbox']");
        if (checkbox.checked) {
            file_name.push(file.textContent);
        }
    });
    if (!file_name[0]){
        alert("No file choose!")
        return
    }
    await fetch("/delete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({  "filenames": file_name }),
    });

    load_doc()
})

// Voice recording state
let isRecording = false;
const micButton = document.getElementById('mic');

micButton.addEventListener('click', async function() {
    const file_name = [];
    const file_items = document.querySelectorAll(".file-item");
    
    // Collect the names of selected files
    file_items.forEach(file => {
        const checkbox = file.querySelector("input[type='checkbox']");
        if (checkbox.checked) {
            file_name.push(file.textContent);
        }
    });
    
    if (!file_name.length) {
        alert("Please select at least one file!");
        return;
    }

    isRecording = !isRecording;
    
    if (isRecording) {
        micButton.classList.add('recording');
        // Start recording logic here
        console.log('Recording started');
        
        try {
            const response = await fetch("/mic", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ "file_name": file_name }),
            });
            
            const data = await response.json();
            
            // Add user message (voice input)
            add_new_message("Voice input");
            
            // Add bot response
            add_new_respone(data.response);
            
            // Scroll to bottom
            const chatShow = document.querySelector(".chat-show");
            chatShow.scrollTop = chatShow.scrollHeight;
            
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred while processing voice input");
        } finally {
            // Reset recording state
            isRecording = false;
            micButton.classList.remove('recording');
        }
    } else {
        micButton.classList.remove('recording');
        // Stop recording logic here
        console.log('Recording stopped');
    }
});

// Hàm cuộn xuống cuối chat
function scrollToBottom() {
    const chatMessages = document.querySelector('.chat-messages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Hàm hiển thị tin nhắn với hiệu ứng gõ từng ký tự
function displayMessageWithTypingEffect(message, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    if (isUser) {
        // Hiển thị ngay lập tức cho tin nhắn người dùng
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        // Cuộn xuống sau khi hiển thị tin nhắn người dùng
        setTimeout(scrollToBottom, 100);
    } else {
        // Thêm placeholder cho tin nhắn bot
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'typing-indicator';
        typingIndicator.innerHTML = '<span></span><span></span><span></span>';
        messageDiv.appendChild(typingIndicator);
        chatMessages.appendChild(messageDiv);
        
        // Cuộn xuống khi hiển thị typing indicator
        setTimeout(scrollToBottom, 100);
        
        // Xóa typing indicator sau 1 giây
        setTimeout(() => {
            typingIndicator.remove();
            
            // Hiển thị từng ký tự một
            let index = 0;
            
            function typeNextChar() {
                if (index < message.length) {
                    messageDiv.textContent += message[index];
                    index++;
                    // Cuộn xuống sau mỗi ký tự
                    scrollToBottom();
                    
                    // Thêm độ trễ ngẫu nhiên giữa các ký tự (30-70ms)
                    const delay = Math.random() * 40 + 30;
                    setTimeout(typeNextChar, delay);
                } else {
                    // Cuộn xuống lần cuối sau khi hiển thị xong
                    setTimeout(scrollToBottom, 100);
                }
            }
            
            // Bắt đầu gõ ký tự đầu tiên
            typeNextChar();
        }, 1000);
    }
}

// Thêm sự kiện cuộn xuống khi có tin nhắn mới
document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.querySelector('.chat-container');
    const observer = new MutationObserver(() => {
        scrollToBottom();
    });
    
    observer.observe(chatContainer, {
        childList: true,
        subtree: true
    });
});

// Cập nhật hàm sendMessage để sử dụng hiệu ứng gõ
async function sendMessage() {
    const message = messageInput.value.trim();
    if (message === '') return;

    // Hiển thị tin nhắn người dùng
    displayMessageWithTypingEffect(message, true);
    messageInput.value = '';

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        // Hiển thị phản hồi với hiệu ứng gõ
        displayMessageWithTypingEffect(data.response);
    } catch (error) {
        console.error('Error:', error);
        displayMessageWithTypingEffect('Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại sau.');
    }
}

// Cập nhật hàm handleVoiceInput để sử dụng hiệu ứng gõ
async function handleVoiceInput(transcript) {
    // Hiển thị tin nhắn người dùng
    displayMessageWithTypingEffect(transcript, true);

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: transcript }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        // Hiển thị phản hồi với hiệu ứng gõ
        displayMessageWithTypingEffect(data.response);
    } catch (error) {
        console.error('Error:', error);
        displayMessageWithTypingEffect('Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại sau.');
    }
}
