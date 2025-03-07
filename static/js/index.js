const add_data = document.getElementById("add-data");
const add_pdf = document.getElementById("add-pdf");

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
