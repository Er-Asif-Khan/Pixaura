// particles.js (updated to sync with light/dark theme)
const canvas = document.createElement("canvas");
document.body.appendChild(canvas);
const ctx = canvas.getContext("2d");

canvas.style.position = "fixed";
canvas.style.top = 0;
canvas.style.left = 0;
canvas.style.zIndex = -1;

let w, h;
function resize() {
  w = canvas.width = window.innerWidth;
  h = canvas.height = window.innerHeight;
}
resize();
window.addEventListener("resize", resize);

const particles = [];
for (let i = 0; i < 80; i++) {
  particles.push({
    x: Math.random() * w,
    y: Math.random() * h,
    r: Math.random() * 2 + 1,
    dx: (Math.random() - 0.5) * 0.5,
    dy: (Math.random() - 0.5) * 0.5
  });
}

let particleColor = "#fff"; // default for dark mode

function isLightMode() {
  const html = document.documentElement;
  // Prefer explicit dataset if set by your theme.js
  if (html.dataset.theme) return html.dataset.theme === "light";
  // Fallback to class used by your theme.js
  if (html.classList.contains("light-mode")) return true;
  if (document.body && document.body.classList.contains("light-mode")) return true;
  // Final fallback to saved preference
  return localStorage.getItem("theme") === "light";
}

function updateParticleColor() {
  particleColor = isLightMode() ? "#000" : "#fff";
}

// Observe theme changes on <html> and <body>
const obsOptions = { attributes: true, attributeFilter: ["class", "data-theme"] };
new MutationObserver(updateParticleColor).observe(document.documentElement, obsOptions);
if (document.body) new MutationObserver(updateParticleColor).observe(document.body, obsOptions);

// Also react to cross-tab/localStorage updates
window.addEventListener("storage", (e) => {
  if (e.key === "theme") updateParticleColor();
});

// Initial color set
updateParticleColor();

function draw() {
  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = particleColor;
  particles.forEach(p => {
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.fill();

    p.x += p.dx;
    p.y += p.dy;

    if (p.x < 0 || p.x > w) p.dx *= -1;
    if (p.y < 0 || p.y > h) p.dy *= -1;
  });

  requestAnimationFrame(draw);
}
draw();