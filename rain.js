const canvas = document.getElementById('rain-canvas');
let ctx = null;
let width, height, raindrops = [];
const dpr = window.devicePixelRatio || 1;

function init() {
    ctx = canvas.getContext('2d');
    if (!ctx) return;

    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.setAttribute('aria-hidden', 'true');
    canvas.setAttribute('role', 'img');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    raindrops = [];
    const count = Math.floor(width / 4);
    for (let i = 0; i < count; i++) {
        raindrops.push({
            x: Math.random() * width,
            y: Math.random() * height,
            length: Math.random() * 20 + 10,
            speed: Math.random() * 10 + 10,
            opacity: Math.random() * 0.3 + 0.1
        });
    }
}

function animate() {
    if (!ctx) return;
    ctx.clearRect(0, 0, width, height);
    ctx.strokeStyle = 'rgba(174, 194, 224, 0.5)';
    ctx.lineWidth = 1;
    
    raindrops.forEach(r => {
        ctx.beginPath();
        ctx.moveTo(r.x, r.y);
        ctx.lineTo(r.x, r.y + r.length);
        ctx.stroke();
        
        r.y += r.speed;
        if (r.y > height) {
            r.y = -r.length;
            r.x = Math.random() * width;
        }
    });
    requestAnimationFrame(animate);
}

window.addEventListener('resize', () => {
    init();
});

document.addEventListener('DOMContentLoaded', () => {
    init();
    animate();
});