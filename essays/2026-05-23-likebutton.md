# いいねボタンの導入

2026/05/23 / JavaScript / Firebase

## About this Project

Vercel等でホスティングされる静的なポートフォリオサイトは、高速かつ低コストで運用可能だが、動的なインタラクション（評価やコメント等）を導入する際にはサーバーサイドが必要になる。 

本プロジェクトでは、GoogleのBaaSである **Firebase Cloud Firestore**とクライアントサイドの **JavaScript **を組み合わせることで、完全なサーバーレス構成にて、安全で軽量な「いいねボタン（インクリメント評価）」機能を実装した。

## System Architecture

### 1. Firestoreのデータ構造

いいね数は、ページごとの識別子（パス名から生成）をドキュメントIDとして管理し、アトミックなインクリメント処理を行います。 


- **コレクション名: **`likes `
- **ドキュメントID: **`pageId `（例: `android_auto_music_player `） 
- **フィールド: **`{ count: number } `

### 2. 重複防止のフロー


- 1. ページロード時、ローカルストレージ（ `liked__pageId `）に値があるかチェックする。 
- 2. 値が存在すれば、ボタンに `liked `クラスを追加し、アイコンを「♥」にする（再度クリックできないようにガードする）。 
- 3. クリックされた際、まだ「いいね」されていなければ、ローカルストレージにフラグを書き込み、Firestoreサーバーに対してインクリメント（+1）リクエストを送信する。

## Core Implementation

### JavaScriptによる同期処理 (`like.js` 抜粋)

Firestoreの `increment `演算子を使用することで、複数のユーザーが同時にクリックしてもカウントが正確に更新（アトミック操作）される設計となっています。 


```
`import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js';
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
} `
```

## Security Design & Best Practices

フロントエンドにAPIキーを公開することから、Firestoreのセキュリティとリソース保護は主に以下の2つのレイヤーで防御しています。 

### 1. Firestoreセキュリティルール

何者かが他人のドキュメントを勝手に削除したり、カウントを大幅に改ざんしたりできないよう、Firebaseコンソール上で強固なアクセス制限を記述しています。 


```
`rules_version = '2';
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

### 2. APIキーのHTTPリファラー制限

Google Cloudコンソール側の設定において、APIキーが使用できるWebサイトのドメイン（HTTPリファラー）を `https://amekusa.vercel.app/* `に限定する制限を適用しています。これにより、第三者がAPIキーをそのままコピーして別ドメインで再利用することを技術的に防ぐ仕組みになっています。

## Conclusion

サーバーレス技術（BaaS）とクライアントJSの工夫により、個人ポートフォリオ等の静的サイトでも安全・低コストに動的なコミュニケーション機能を導入できることが確認できました。 

現在、本機能は「雨草の庭」内のすべての記事・解説ページに標準実装されており、訪問者からの有益なフィードバックとして役立てられています。
