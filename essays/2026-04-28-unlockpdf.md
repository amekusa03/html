# Gmail PDF Unlocker

2026/04/28  Python / VM

仮想マシンによる、メールの自動処理

## About this Project

メールし、設定した条件のメールであれば、添付ファイルのPDFをパスワードを解除してGoogleドライブに保存する、というプロジェクトです。

## System Configuration & Workflow

Google Apps Script (GAS) ではなく Python を採用することで、仕様変更にも柔軟な対応を可能としています。 


- ***iaas: **Google Compute Engine (GCE)
                            の無料枠（e2-micro） 
- ***言語: **Python 
- ***対象メール: **特定の送信元からの未読メール 
- ***処理内容: **添付PDFのパスワード保護を自動解除 
- ***保存先: **Googleドライブの指定フォルダ 
- ***後処理: **処理済みラベル付与と既読化 
GCE の `e2-micro `インスタンスを利用することで、実質無料で常時運用が可能です。※1 


- **Gmail API: **特定の送信元から届く未読メールを検索・取得。 
- **Python (pypdf): **メモリ上で安全にPDFのパスワードを解除。 
- **Google Drive API: **指定したフォルダへ自動的に保存。 
※1 以前の無料枠対象だった f1-micro と間違えないようご注意ください。e2-micro が現在の無料枠対象です。

## Setup

#### 1. GCP プロジェクトの設定


1. Gmail API と Google Drive API を有効化。 
2. OAuth 同意画面を設定し、デスクトップアプリとして「OAuth クライアント ID」を作成。 
3. `credentials.json `を取得。 

#### 2. インストールと配置


```
`git clone <your-repo-url>
cd unlockpdf
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt `
```

## Usage

#### 初回実行（認証）

初回実行時はブラウザが立ち上がり、Googleアカウントへのログインが求められます。認証が完了すると、作業ディレクトリに `token.json `が生成されます。 


```
`python unlock_and_save.py `
```

#### サービス化 (systemd)

24時間365日、常時稼働させるために Linux の `systemd `を使用してバックグラウンドプロセスとして登録します。これにより、プログラムの異常終了時やサーバー再起動時にも自動で復帰します。 


```
`# /etc/systemd/system/unlockpdf.service
[Service]
ExecStart=/path/to/venv/bin/python /path/to/unlock_and_save.py
Restart=always
User=your-user-name `
```

## Deployment (Google Compute Engine)

コストを最適化(最小化)するため、GCE の無料枠（e2-micro）での運用します。 


1. **インスタンス作成: **無料枠対象リージョン（us-west1, us-central1 など）で `e2-micro `を作成。 (⚠️私は f1-microで 作成してしまい、課金が発生してしまいました。料金計算は数時間遅れるため、停止後もしばらくは料金が 増加します） 
2. **ファイルの転送: **`unlock_and_save.py `, `credentials.json `, `token.json `をアップロード。 ※ サーバーはGUIがないため、ローカル環境で生成した `token.json `を転送する必要があります。 


3. **常時稼働の設定: **`systemd `ユニットファイルを作成し、サービスを有効化（enable/start）します。

## Security Considerations

***重要：認証情報の保護 **

以下の秘匿情報は、絶対に GitHub 等の公開リポジトリに含めないでください。環境変数の利用を強く推奨します。 


- `credentials.json `（アプリの鍵） 
- `token.json `（アカウントのアクセス権） 
- `PDF_PASSWORD `（生パスワード） 
誤って公開してしまった場合は、速やかに該当のクレデンシャルを無効化し、新しいものを発行してください。

## Development Environment

- Google Compute Engine 
- Python 3.x 
- Gmail & Drive API 
- pypdf

## Precautions & Resources

**Google Cloud Platformの料金 **にご注意ください。無料枠（e2-micro）の範囲外で運用すると課金が発生します。 

資料はGitHubで公開しています。個人の学習や小規模なプロジェクトでの再利用を歓迎します。 

[View on GitHub](https://github.com/amekusa03/AskGeminibyemail)

## Best Practices for 24/7 Operation

#### 1. プロセス管理 (systemd)

OS起動時やクラッシュ時に自動再起動させるため、 `systemd `でサービス化するのが最も堅牢です。 


```
`[Service]
Restart=always
RestartSec=5
ExecStart=/path/to/venv/bin/python main.py `
```

#### 2. Pythonコードの堅牢化


- **例外処理: **メインループを `try-except `で囲み、一時的なエラーで停止しないようにします。 
- **ロギング: **`logging `ライブラリを使用し、Google Cloud Logging
                                で遠隔から状態を確認可能にします。 

#### 3. インフラの安定化


- **メモリ監視: **e2-micro はメモリが少なめ（1GB）なため、OOM Killerによる停止に注意が必要です。 
- **静的IP: **通信を安定させるため、静的外部IPアドレスの予約を推奨します。 
- **自動更新: **GCEのOS構成管理機能でセキュリティパッチ適用を自動化します。 

#### 4. コンテナ化の検討

将来的な環境移行やスケーリングを見据え、Dockerコンテナ化してデプロイすることで、依存関係のトラブルを最小限に抑えられます。
