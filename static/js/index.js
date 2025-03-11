const add_data = document.getElementById("add-data");
const add_pdf = document.getElementById("add-pdf");
const send = document.getElementById("send")
let chat = document.getElementById("chat-input")
add_data.addEventListener("click", function () {
    add_pdf.click();
});

// Xử lý sự kiện khi chọn file
add_pdf.addEventListener("change", function (event) { // Đổi từ "click" thành "change"
    const file = event.target.files[0]; // Sửa từ "file" thành "files"

    if (!file) {
        alert("No file chosen!"); // Sửa lỗi chính tả
        return;
    }

    const formData = new FormData();
    formData.append("file", file); // Sửa từ fileObject thành file

    fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => console.log("Success:", data))
    .catch(error => console.error("Error:", error));
});

send.addEventListener("click", async function(){
    const message = chat.value 
    chat.value = null
    if (!message.trim()) return;
    add_new_message(message)
    await fetch("/user", {
        method: "POST",
        body: JSON.stringify({ "message": message }),
    });
})

async function load_message() {
    const response = await fetch("/load_all");
    const datas = await response.json();

    if (!datas) return;
    console.log(datas)
    const chatShow = document.querySelector(".chat-show");
    chatShow.innerHTML = ""; // Xóa nội dung cũ

    datas.forEach((data) => {
        const messageuserDiv = document.createElement("div"); // message from user
        const messageresponeDiv = document.createElement("div"); // message from model ai
        messageuserDiv.classList.add("message-box");

        messageuserDiv.classList.add("user-message");
        messageresponeDiv.classList.add("bot-response");

        messageuserDiv.textContent = data.message;
        messageresponeDiv.textContent = data.response;

        chatShow.appendChild(messageuserDiv); // add user meesage
        chatShow.appendChild(messageresponeDiv); // add respone model
    });

    // Cuộn xuống cuối cùng để hiển thị tin nhắn mới nhất
    chatShow.scrollTop = chatShow.scrollHeight;
}

load_message()

function add_new_message(message){
    const chatShow = document.querySelector(".chat-show");

    const messageuserDiv = document.createElement("div"); // message from user
    messageuserDiv.classList.add("message-box");

    messageuserDiv.classList.add("user-message");

    messageuserDiv.textContent = message;

    chatShow.appendChild(messageuserDiv); // add user meesage
}
