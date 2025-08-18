function adjustBubble(bubble, head, imgWidth, imgHeight, scaleX, scaleY, isLeft) {
    let bw = head.bubble_width * scaleX;
    let bh = bw;
    let fontSize = head.font_size;

    let x, y;
    if (isLeft) {
      x = head.top_l[0] * scaleX - bw;
      y = head.top_l[1] * scaleY - (bw * 0.6);
    } else {
      const topRightX = head.bottom_r[0];
      const topRightY = head.top_l[1];
      x = topRightX * scaleX;
      y = topRightY * scaleY - (bw * 0.6);
    }

    let tries = 0;
    while (tries < 50) {
      let overlapsHead = !(x + bw < head.top_l[0] * scaleX || x > head.bottom_r[0] * scaleX || y + bh < head.top_l[1] * scaleY || y > head.bottom_r[1] * scaleY);
      
      let touchesEdge = false;

      if (isLeft) {
        if (x < 0) { touchesEdge = true; x += 5; }
        if (y < 0) { touchesEdge = true; y += 5; }
        if (overlapsHead) {
          if (x + bw > head.top_l[0] * scaleX) x -= 5;
          if (y + bh > head.top_l[1] * scaleY) y -= 5;
        }
      } else {
        if (x + bw > imgWidth) { touchesEdge = true; x -=5; }
        if (y < 0) { touchesEdge = true; y += 5; }
        if (overlapsHead) {
          if (x < head.bottom_r[0] * scaleX) x += 5;
          if (y + bh > head.top_l[1] * scaleY) y -= 5;
        }
      }

      if (touchesEdge && overlapsHead) {
        bw *= 0.9;
        bh = bw;
        fontSize *= 0.9;
      }

      if (!overlapsHead && x >= 0 && y >= 0 && x + bw <= imgWidth && y + bh <= imgHeight) break;

      tries++;
    }

    bubble.style.left = x + "px";
    bubble.style.top = y + "px";
    // bubble.style.width = (bw * 2) + "px";
    bubble.style.fontSize = (fontSize * 1.15) + "px";
}

document.getElementById('comicForm').addEventListener('submit', function(e) {
e.preventDefault();

const formData = new FormData();
const fileInput = document.getElementById('fileInput');
const genre = document.getElementById('genre').value;
if (!fileInput.files.length) return alert("Please select an image");
formData.append('image', fileInput.files[0]);
formData.append('genre', genre);
fetch('./comicgen', { method: 'POST', body: formData })
  .then(res => res.json())
  .then(data => {
    if (data.error) {
      alert(data.error);
      return;
    }
    const previewImage = document.getElementById('previewImage');
    const bubblesLayer = document.getElementById('bubblesLayer');
    const downloadBtn = document.getElementById('downloadBtn');

    const reader = new FileReader();
    reader.onload = function(e) {
      previewImage.src = e.target.result;

      previewImage.onload = function() {
        bubblesLayer.innerHTML = ""; // Clear old bubbles
        
        const imgWidth = previewImage.width;
        const imgHeight = previewImage.height;
        const scaleX = imgWidth / data.original_width;
        const scaleY = imgHeight / data.original_height;

        data.heads.forEach((headData, index) => {
          const bubble = document.createElement('div');
          bubble.classList.add('bubble');
          bubble.classList.add(index === 0 ? 'left' : 'right');
          bubble.textContent = headData.text;
        
          bubblesLayer.appendChild(bubble);
          adjustBubble(bubble, headData, imgWidth, imgHeight, scaleX, scaleY, index === 0);
        });

        downloadBtn.style.display = "inline-block";
      };
    };
    reader.readAsDataURL(fileInput.files[0]);
  })
  .catch(err => {
    console.error(err);
    alert("Error generating comic bubbles");
  });
});

document.getElementById('downloadBtn').addEventListener('click', function() {
  const container = document.getElementById('comicContainer');
  html2canvas(container, { backgroundColor: null }).then(canvas => {
    const link = document.createElement('a');
    link.download = "comic_image.png";
    link.href = canvas.toDataURL("image/png");
    link.click();
  });
});