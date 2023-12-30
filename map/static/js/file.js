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

function addSelectMenuEventListeners(optionMenu, index) {
    var selectBtn = optionMenu.querySelector(".select-btn");
    var options = optionMenu.querySelectorAll(".option");
    var sBtn_text = optionMenu.querySelector(".sBtn-text");
    var hiddenInput = optionMenu.querySelector("#program_type_" + index);

    selectBtn.addEventListener("click", () => optionMenu.classList.toggle("active"));

    options.forEach(option => {
        option.addEventListener("click", () => {
            let selectedOption = option.querySelector(".option-text").innerText;
            sBtn_text.innerText = selectedOption;

            let value = option.getAttribute("data-value");
            hiddenInput.value = value;

            optionMenu.classList.remove("active");
        });
    });
}

var optionMenus = document.querySelectorAll(".select-menu");
optionMenus.forEach((optionMenu, index) => {
    addSelectMenuEventListeners(optionMenu, index);
});

window.onload = function() {
    const selectedOptions = document.querySelectorAll(".option[selected]");
    selectedOptions.forEach(selectedOption => {
        const selectedText = selectedOption.querySelector(".option-text").innerText;
        const selectedValue = selectedOption.getAttribute("data-value");
        const sBtn_text = selectedOption.closest('.select-menu').querySelector(".sBtn-text");
        const hiddenInput = selectedOption.closest('.select-menu').querySelector(".program-type-input");
        sBtn_text.innerText = selectedText;
        hiddenInput.value = selectedValue;
    });
}

document.getElementById('add-program').addEventListener('click', function() {
    var programContainer = document.getElementById('program-container');
    var programFields = document.querySelector('.program-fields');
    var newProgramFields = programFields.cloneNode(true);

    var numProgramFields = programContainer.getElementsByClassName('program-fields').length;

    var inputs = newProgramFields.querySelectorAll('input');
    inputs = Array.from(inputs).filter(node => node.nodeType === Node.ELEMENT_NODE);
    for (var i = 0; i < inputs.length; i++) {
        inputs[i].name = inputs[i].name.replace(/_0/, '_' + numProgramFields);
        inputs[i].id = inputs[i].id.replace(/_0/, '_' + numProgramFields);
        inputs[i].value = '';
    }

    var hiddenInput = newProgramFields.querySelector('input[type="hidden"]');
    hiddenInput.id = hiddenInput.id.replace(/_0/, '_' + numProgramFields);

    var selectBtn = newProgramFields.querySelector(".sBtn-text");
    selectBtn.textContent = "Select Program";

    programContainer.appendChild(newProgramFields);

    var newOptionMenu = newProgramFields.querySelector(".select-menu");
    addSelectMenuEventListeners(newOptionMenu, numProgramFields);

    document.getElementById('remove-program').disabled = false;
});

document.getElementById('remove-program').addEventListener('click', function() {
    var programContainer = document.getElementById('program-container');
    var programFields = programContainer.getElementsByClassName('program-fields');
    var removeProgramButton = document.getElementById('remove-program');

    if (programFields.length > 1) {
        programContainer.removeChild(programFields[programFields.length - 1]);
    }

    if (programFields.length <= 1) {
        removeProgramButton.disabled = true;
    }
});

function geocodeAddress() {
    var address = document.querySelector('input[name="location"]').value;
    fetch(`https://geocode.search.hereapi.com/v1/geocode?q=${address}&apiKey=szrQPzoAGEM6OAnlea5YEQa8LkILYDP3QBv--ehKuKM`)
        .then(response => response.json())
        .then(data => {
            document.querySelector('input[name="latitude"]').value = data.items[0].position.lat;
            document.querySelector('input[name="longitude"]').value = data.items[0].position.lng;
        })
        .catch(error => console.error('Error:', error));
}






