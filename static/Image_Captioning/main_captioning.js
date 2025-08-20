const selectBtn = document.getElementById('selectBtn');
const fileInput = document.getElementById('fileInput');
const dropZone = document.getElementById('dropZone');
const fileList = document.getElementById('fileList');
const mergeBtn = document.getElementById('mergeBtn');
const uploadArea = document.querySelector('.upload-area');
const fileChosen = document.getElementById("fileChosen");

let selectedFiles = [];

// File selection
selectBtn.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
        fileChosen.textContent = fileInput.files[0].name;
        fileChosen.classList.add("active");
    } else {
        fileChosen.textContent = "No file chosen";
        fileChosen.classList.remove("active");
    }
});

// Drag and drop functionality
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    if (!uploadArea.contains(e.relatedTarget)) {
        dropZone.classList.remove('drag-over');
    }
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    handleFiles(e.dataTransfer.files);
});

function handleFiles(files) {
    if (files.length > 0) {
        // Create a DataTransfer to assign dropped file to file input
        const dataTransfer = new DataTransfer();
        for (let i = 0; i < files.length; i++) {
            dataTransfer.items.add(files[i]);
        }
        fileInput.files = dataTransfer.files; // Now input has the dropped file(s)

        // Update text
        fileChosen.textContent = files[0].name;
        fileChosen.classList.add("active");
    } else {
        fileChosen.textContent = "No file selected";
        fileChosen.classList.remove("active");
    }
}



function copyCaption() {
    const caption = document.getElementById("caption-text").innerText;
    navigator.clipboard.writeText(caption).then(() => {
        alert("✅ Caption copied to clipboard!");
    }).catch(err => {
        alert("❌ Failed to copy: " + err);
    });
}
