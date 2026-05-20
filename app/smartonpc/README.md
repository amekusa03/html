# SmartOn PC

ESP32-C3 を使い、Ubuntu PCをスマートホームデバイスとして **Matter** プロトコルで制御するファームウェアです。  
Google Home / Nest Hub からの音声操作や自動化でPCの電源をON/OFFできます。

---

## 実装ステップ

| ステップ | 内容 | 状態 |
|---------|------|------|
| Step 1 | Matter ON/OFF 制御（電源ボタン押下） | ✅ 実装済み |
| Step 2 | PC電源状態監視 + Matter 属性同期 | ✅ 実装済み |

## 機能

### Step 1

| 機能 | 手段 |
|------|------|
| 電源ON | メカリレー → 電源ボタン短押し（500ms） |
| 電源OFF | メカリレー → 電源ボタン短押し（500ms）+ Ubuntu ACPI設定でシャットダウン |
| ファクトリーリセット | GPIO9 長押し（3秒） |

- **WoL（Wake on LAN）は不採用** — 信頼性の問題による
- **電源OFF**: リレーで電源ボタンを短押しし、Ubuntu の ACPI 設定（`HandlePowerKey=poweroff`）が正常シャットダウンを開始する

### Step 2

| 機能 | 手段 |
|------|------|
| 電源状態検出 | PC817 経由で電源 LED を GPIO 入力（アクティブLOW） |
| 乖離検出 | 2秒ポーリング、3回連続で確定 |
| Matter 属性同期 | 乖離確定時に `attribute::update()` で OnOff 属性を実態に合わせる |
| ユーザー通知 | Matter サブスクリプション経由（Google Home 等が自動受信） |

**フェイルセーフ原則**: 乖離を検出してもシステムは自動での ON/OFF 操作を行わない。実態を Matter 属性に反映してユーザーへ委ねる。

---

## ハードウェア構成

- **マイコン**: Generic ESP32-C3
- **ホストPC**: Ubuntu
- **電源制御**: メカリレー経由でマザーボードの PWR SW ピンを短絡
- **電源状態検出**: PC817 フォトカプラ経由で電源 LED を読み取る
- **コントローラー**: Google Nest Hub / Android スマートフォン

### GPIO割り当て

| GPIO | 役割 | 回路 |
|------|------|------|
| GPIO 20 | OUTPUT: PWR SW制御 | メカリレー経由 |
| GPIO 4  | INPUT: PWR LED検出 | PC817 フォトカプラ経由（アクティブLOW） |
| GPIO 9  | INPUT: ファクトリーリセット | 内部プルアップ、LOW=押下 |

### 回路図

**PWR SW（GPIO 20 → メカリレー → マザーボード）**
```
GPIO 20 → リレー制御入力
リレー接点 → マザーボード PWR SW ヘッダ短絡
```

**PWR LED（マザーボード → PC817 → GPIO 4）**
```
PWR_LED+ → 470Ω → PC817 Anode(pin1)
PC817 Cathode(pin2) → PWR_LED- (GND)
3.3V → 10kΩ → PC817 Collector(pin4) → GPIO 4
PC817 Emitter(pin3) → GND

PC ON  : LED点灯 → PC817導通 → GPIO = LOW
PC OFF : LED消灯 → PC817遮断 → GPIO = HIGH (pullup)
```

極性は `pc_control.c` の `PWR_SW_ACTIVE_HIGH` マクロで切り替え可能。

---

## ソフトウェアスタック

| レイヤー | 名称 | バージョン |
|---------|------|-----------|
| OS / SDK | ESP-IDF | 5.4.1 |
| Matter ラッパー | esp-matter | `$ESP_MATTER_PATH` で指定 |
| Matter 本体 | ConnectedHomeIP (CHIP) | esp-matter サブモジュール |

Matterデバイスタイプ: **On/Off Plug-in Unit**

---

## ビルド

### 前提条件

- ESP-IDF 5.4.1 がセットアップ済み
- esp-matter がセットアップ済み（`ESP_MATTER_PATH` 環境変数に設定）

### WiFi認証情報の設定

`main/wifi_creds.h` を作成してSSIDとパスワードを記載します（`.gitignore` 済み）:

```c
#define WIFI_SSID     "your-ssid"
#define WIFI_PASSWORD "your-password"
```

### ビルド & フラッシュ

```bash
. $IDF_PATH/export.sh
. $ESP_MATTER_PATH/export.sh
export _PW_ACTUAL_ENVIRONMENT_ROOT

idf.py set-target esp32c3
idf.py build
idf.py -p /dev/ttyACM0 flash
```

### Matterコミッショニング

フラッシュ後、シリアルモニタにQRコードとセットアップPINが出力されます。  
Google Home アプリ等でスキャンしてデバイスを登録してください。

開発・テスト段階ではテスト用DAC（Device Attestation Certificate）を使用します。

**テスト用セットアップコード**（`CONFIG_ENABLE_TEST_SETUP_PARAMS=y` による固定値）

| 項目 | 値 |
|------|-----|
| Manual Pairing Code | `34970112332` |
| Setup PIN | `20202021` |
| Discriminator | `3840` |

---

## 設計上の判断

### BLE無効化・WiFiオンリーコミッショニング

`sdkconfig.defaults` で BLE を完全に無効化している（`CONFIG_BT_ENABLED=n`, `CONFIG_ENABLE_CHIPOBLE=n`）。

**理由**: `store_wifi_credentials()` でWiFi認証情報をハードコードしているため、デバイスは起動と同時にWiFi接続を試みる。
この状態でCHIPoBLE（MatterのBLEアドバタイズ）が動作すると、BLE/WiFi無線の競合によりWiFi接続が完全に阻害される。

**結論**: WiFi認証情報を事前に埋め込む設計においては、BLEを無効化してIPネットワーク経由コミッショニング（`kOnNetwork`）に統一するのが正しい。

コミッショニングはQRコードまたはManual Pairing Codeで行う（シリアルモニタに出力される）。

### フェイルセーフ原則（乖離検出時の動作）

Matter 仕様の前提は「実態が確定的に判定できていること」。乖離時の自動 ON/OFF は誤動作リスクを生む。

> **安全な方向 = 操作しない。判断はユーザーに委ねる。**

乖離確定（3回連続ポーリングで不一致）時の動作:
1. `attribute::update()` で OnOff 属性を実態に同期
2. Matter サブスクリプション経由でコントローラー（Google Home 等）へ通知
3. システムは電源ボタンを操作しない

---

## 既知の問題 / 課題

### mDNS 競合（解消済み）

旧実装（Ping ベースの死活監視）では ESP-IDF `mdns_init()` と Matter 内部 mDNS がポート 5353 で競合していた。  
**現在は GPIO による電源 LED ポーリングに置き換えたため、mDNS は不使用。問題は解消済み。**

### フリーズ自動回復（未実装）

電源 LED が ON のまま PC が応答しない（フリーズ）ケースは、現状では検出できない。  
手動対応が必要。将来的には Ping との組み合わせ、またはウォッチドッグ的な手段を検討。

---

## ライセンス

本プロジェクトのアプリケーションコード（`main/`）は [Apache License 2.0](LICENSE) です。  
使用している依存コンポーネントも同ライセンス（一部 MIT）です。詳細は [doc/spec.md](doc/spec.md) を参照。
