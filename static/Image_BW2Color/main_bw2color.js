const selectBtn = document.getElementById('selectBtn');
const fileInput = document.getElementById('fileInput');
const dropZone = document.getElementById('dropZone');
const fileList = document.getElementById('fileList');
const mergeBtn = document.getElementById('mergeBtn');
const uploadArea = document.querySelector('.upload-area');

let selectedFiles = [];

// File selection
selectBtn.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
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


function displayFiles() {
    fileList.innerHTML = '';
    
    selectedFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.innerHTML = `
            <div class="file-info">
                <div class="file-icon">📄</div>
                <div class="file-details">
                    <h4>${file.name}</h4>
                    <p>${formatFileSize(file.size)}</p>
                </div>
            </div>
            <button class="remove-btn" onclick="removeFile(${index})">✕</button>
        `;
        fileList.appendChild(fileItem);
    });

    // Show merge button if files are selected
    if (selectedFiles.length > 1) {
        mergeBtn.classList.add('show');
    } else {
        mergeBtn.classList.remove('show');
    }
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
    displayFiles();
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}


// Mobile menu toggle
const menuIcon = document.querySelector('.menu-icon');
const navLinks = document.querySelector('.nav-links');

menuIcon.addEventListener('click', () => {
    navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
});

// Make removeFile function global
window.removeFile = removeFile;
