const add_data = document.getElementById("add-data")
const add_pdf = document.getElementById("add-pdf")
add_data.addEventListener("click", function(){
    add_pdf.click()
})

// add data from file pdf
add_pdf.addEventListener("click", function(event){
    const file = event.target.file[0] // add data from file upload
    if(!file){
        alert("No file chose!!!!") // if havn't data upload
        return
    }

    const file_name = file.name // add file name

    const formData = new FormData();
    formData.append(`${file_name}`, fileObject); // add file

    fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
    });
})