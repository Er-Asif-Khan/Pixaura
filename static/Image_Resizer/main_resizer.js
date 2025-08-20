const fileInput = document.getElementById('fileInput');
const dropZone = document.getElementById('dropZone');
const uploadArea = document.getElementById('uploadArea');

const uploadBtn = document.getElementById('uploadBtn');
const filePreview = document.getElementById('filePreview');
const previewImg = document.getElementById('previewImg');
const previewImg2 = document.getElementById('previewImg2');
const imageInfo = document.getElementById('imageInfo');
const imageInfo2 = document.getElementById('imageInfo2');
const resizeParams = document.getElementById('resizeParams');
const widthInput = document.getElementById('widthInput');
const heightInput = document.getElementById('heightInput');
const maintainAspect = document.getElementById('maintainAspect');
const resizeBtn = document.getElementById('resizeBtn');
const downloadLink = document.getElementById('downloadLink');
const resizeForm = document.getElementById('resizeForm');
const fileChosen = document.getElementById("fileChosen");
const outputSection = document.getElementById("outputSection");

let selectedFile = null;
let originalDimensions = {};

// File selection
uploadBtn.addEventListener('click', () => {
    fileInput.click();
});

// Drag and drop functionality
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    if (!uploadArea.contains(e.relatedTarget)) {
        dropZone.classList.remove('dragover');
    }
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
        fileInput.files = e.dataTransfer.files;
        handleFile(e.dataTransfer.files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) {
        handleFile(e.target.files[0]);
    }
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


function handleFile(file) {
    if (!file.type.startsWith('image/')) {
        alert('Please select an image file.');
        return;
    }

    selectedFile = file;
    
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        previewImg.style.display = 'block';
        
        previewImg.onload = () => {
            originalDimensions = {
                width: previewImg.naturalWidth,
                height: previewImg.naturalHeight
            };
            
            // Set default values
            widthInput.value = previewImg.naturalWidth;
            heightInput.value = previewImg.naturalHeight;
            
            // Update file info
            imageInfo.textContent = `${file.name} • ${previewImg.naturalWidth}×${previewImg.naturalHeight} • ${(file.size / 1024).toFixed(1)}KB`;
            
            // Show resize controls
            resizeParams.classList.add('show');
            downloadLink.style.display = 'none';
        };
    };
    reader.readAsDataURL(file);
}

let isUpdating = false;

widthInput.addEventListener('input', () => {
    if (maintainAspect.checked && !isUpdating && originalDimensions.width) {
        isUpdating = true;
        const aspectRatio = originalDimensions.width / originalDimensions.height;
        heightInput.value = Math.round(widthInput.value / aspectRatio);
        isUpdating = false;
    }
});

heightInput.addEventListener('input', () => {
    if (maintainAspect.checked && !isUpdating && originalDimensions.width) {
        isUpdating = true;
        const aspectRatio = originalDimensions.width / originalDimensions.height;
        widthInput.value = Math.round(heightInput.value * aspectRatio);
        isUpdating = false;
    }
});

resizeBtn.addEventListener('click', () => {
    const width = parseInt(widthInput.value);
    const height = parseInt(heightInput.value);

    if (!width || !height) {
        alert('Please enter valid width and height values.');
        return;
    }

    if (!selectedFile) {
        alert('Please select an image first.');
        return;
    }

    // Create a canvas to resize the image
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');
    
    // Draw the resized image
    ctx.drawImage(previewImg, 0, 0, width, height);

    
    // Update the preview
    previewImg2.src = canvas.toDataURL('image/png');
    
    // Update the download link
    canvas.toBlob((blob) => {
        const url = URL.createObjectURL(blob);
        downloadLink.href = url;
        downloadLink.style.display = 'block';
        downloadLink.download = `resized_${selectedFile.name}`;
    }, 'image/png');
    
    // Update file info
    imageInfo2.textContent = `${selectedFile.name} • ${width}×${height} (resized)`;
    
    outputSection.style.display = "block";
    
});

const toggleBtn = document.getElementById('themeToggle');
toggleBtn.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');
    localStorage.setItem('theme', document.body.classList.contains('light-mode') ? 'light' : 'dark');
});

// Apply saved theme
if (localStorage.getItem('theme') === 'light') {
    document.body.classList.add('light-mode');
}
