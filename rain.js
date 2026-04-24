// rain.js - 雨のアニメーションエフェクト

const canvas = document.getElementById('rain-canvas');
let ctx = null;
let width, height, raindrops = [];
const dpr = window.devicePixelRatio || 1;

// 雨粒の最大数（パフォーマンス調整）
const MAX_DROPS = 200;

function init() {
    if (!canvas) return; // キャンバス要素が存在しない場合のチェック
    ctx = canvas.getContext('2d');
    if (!ctx) return;

    // 先に読み取り（レイアウトの再計算を一度に抑える）
    const w = window.innerWidth;
    const h = window.innerHeight;

    // まとめて書き込み
    width = w;
    height = h;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    canvas.setAttribute('aria-hidden', 'true');
    canvas.setAttribute('role', 'img');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    // 雨粒の初期化（最大数を制限）
    raindrops = [];
    const count = Math.min(Math.floor(w / 4), MAX_DROPS);
    for (let i = 0; i < count; i++) {
        raindrops.push({
            x: Math.random() * w,
            y: Math.random() * h,
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

let resizeTimer;
window.addEventListener('resize', () => {
    // デバウンス処理：連続するリサイズイベントの最後から150ms後に実行
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        init();
    }, 150);
});

document.addEventListener('DOMContentLoaded', () => {
    init();
    animate();
});