# Introduction of like button

2026/05/23 / JavaScript / Firebase

## About this Project

Static portfolio sites hosted on Vercel and other platforms can be operated quickly and at low cost, but when implementing dynamic interactions (e.g. ratings and comments), server-side functionality is required.

In this project, we implemented a secure and lightweight "Like button (incremental rating)" function in a completely serverless configuration by combining Google's BaaS **Firebase Cloud Firestore** and client-side **JavaScript**.

## System Architecture

### 1. Firestore data structure

The number of likes is managed using an identifier for each page (generated from the path name) as a document ID, and is incremented atomically.

- **Collection name:**`likes`
- **Document ID:**`pageId` (e.g. `android_auto_music_player`)
- **Field:**`{ count: number }`

### 2. Duplication prevention flow

- 1. When loading the page, check if there is a value in local storage (`liked__pageId`).
- 1. If the value exists, add the `liked` class to the button and change the icon to "♥" (guard it so that it cannot be clicked again).
- 1. When clicked, if it has not been liked yet, writes a flag to local storage and sends an increment (+1) request to the Firestore server.

## Core Implementation

### Synchronous processing using JavaScript (`like.js` excerpt)

By using Firestore's `increment` operator, the count is updated accurately (atomic operation) even if multiple users click at the same time.

```bash
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js';
import { getFirestore, doc, getDoc, setDoc, increment } from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js';

// Firebase初期化設定
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  projectId: "YOUR_PROJECT_ID",
  // ...その他の設定項目
};
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// いいね処理の実行
async function initLikeButton() {
  const btn = document.getElementById('like-btn');
  const countEl = document.getElementById('like-count');
  // ...（DOM取得と存在確認）

  // ページ識別子 (pageId) の生成
  const path = location.pathname;
  const pageId = path
    .replace(/\/index\.html$/, '/')
    .replace(/\.html$/, '')
    .replace(/^\/|\/$/g, '')
    .replace(/\//g, '__') || 'home';

  const storageKey = 'liked__' + pageId;
  const docRef = doc(db, 'likes', pageId);

  // 初回読み込み
  const snap = await getDoc(docRef);
  countEl.textContent = snap.exists() ? (snap.data().count ?? 0) : 0;

  // クリックイベント
  btn.addEventListener('click', async () => {
    if (localStorage.getItem(storageKey)) return;
    localStorage.setItem(storageKey, '1');
    
    // UIを先行して即時更新（楽観的UI更新）
    btn.classList.add('liked');
    countEl.textContent = parseInt(countEl.textContent || '0') + 1;

    // サーバーへの送信（アトミックなインクリメント処理）
    await setDoc(docRef, { count: increment(1) }, { merge: true });
  });
}
```

## Security Design & Best Practices

Since API keys are exposed on the front end, Firestore's security and resource protection consists of two main layers:

### 1. Firestore Security Rules

We have written strong access restrictions on the Firebase console to prevent someone from arbitrarily deleting other people's documents or significantly tampering with counts.

```bash
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /likes/{pageId} {
      // 誰でもいいね数の閲覧が可能
      allow read: if true;
      // いいね（書き込み）を許可
      allow write: if true;
    }
  }
} `
```

### 2. API key HTTP referrer restrictions

In the settings on the Google Cloud console side, a restriction is applied that limits the website domain (HTTP referrer) for which API keys can be used to `https://amekusa.vercel.app/*`. This technically prevents a third party from copying the API key and reusing it on another domain.

## Conclusion

By using serverless technology (BaaS) and client JS, we were able to confirm that dynamic communication functions can be introduced safely and at low cost even on static sites such as personal portfolios.

Currently, this feature is implemented as standard on all articles and explanation pages in "Rain Grass Garden" and is used as a useful feedback from visitors.
