import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js';
import { getFirestore, doc, getDoc, setDoc, increment } from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js';

// TODO: Firebase コンソール（https://console.firebase.google.com）でプロジェクト作成後、
//       ウェブアプリの設定からコピーして書き換えてください
const firebaseConfig = {
  apiKey: "AIzaSyAru3eFz24cBAnuou8PsI2jFHYbFHWBc6U",
  authDomain: "amekusa-site-916ef.firebaseapp.com",
  projectId: "amekusa-site-916ef",
  storageBucket: "amekusa-site-916ef.firebasestorage.app",
  messagingSenderId: "871496120687",
  appId: "1:871496120687:web:3d9f21140432d23e98909a"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

async function initLikeButton() {
  const btn = document.getElementById('like-btn');
  const countEl = document.getElementById('like-count');
  const iconEl = btn ? btn.querySelector('.like-icon') : null;
  if (!btn || !countEl || !iconEl) return;

  const pageId = location.pathname
    .replace(/^\/|\/$/g, '')
    .replace(/\//g, '__')
    .replace(/\.html$/, '');
  const storageKey = 'liked__' + pageId;
  const docRef = doc(db, 'likes', pageId);

  // カウント読み込み
  try {
    const snap = await getDoc(docRef);
    countEl.textContent = snap.exists() ? (snap.data().count ?? 0) : 0;
  } catch {
    countEl.textContent = '0';
  }

  // すでにいいね済みなら表示を変更
  if (localStorage.getItem(storageKey)) {
    btn.classList.add('liked');
    iconEl.textContent = '♥';
  }

  btn.addEventListener('click', async () => {
    if (localStorage.getItem(storageKey)) return;
    localStorage.setItem(storageKey, '1');
    btn.classList.add('liked');
    iconEl.textContent = '♥';
    countEl.textContent = parseInt(countEl.textContent || '0') + 1;
    try {
      await setDoc(docRef, { count: increment(1) }, { merge: true });
    } catch {
      // Firestore への書き込み失敗（UIは既に更新済み）
    }
  });
}

initLikeButton();
