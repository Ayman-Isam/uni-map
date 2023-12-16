const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("input-file");
const imageView = document.getElementById("img-view");

fileInput.addEventListener("change", uploadImage);

function uploadImage() {
    let imgLink = URL.createObjectURL(fileInput.files[0]);
    imageView.style.backgroundImage = `url(${imgLink})`;
    imageView.textContent = "";
}

dropArea.addEventListener("dragover", function (event) {
    event.preventDefault();
});

dropArea.addEventListener("drop", function (event) {
    event.preventDefault();
    fileInput.files = event.dataTransfer.files;
    uploadImage();
});

const optionMenu = document.querySelector(".select-menu"),
        selectBtn = optionMenu.querySelector(".select-btn"), 
        options = optionMenu.querySelectorAll(".option"), 
        sBtn_text = optionMenu.querySelector(".sBtn-text");

selectBtn.addEventListener("click", () => optionMenu.classList.toggle("active"));

options.forEach(option => {
    option.addEventListener("click", () => {
        let selectedOption = option.querySelector(".option-text").innerText;
        sBtn_text.innerText = selectedOption;
        
        optionMenu.classList.remove("active");
    });
})


