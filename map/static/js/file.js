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

