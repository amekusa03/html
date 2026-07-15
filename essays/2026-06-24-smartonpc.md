# SmartOn PC

2026/06/24 / ESP-IDF / Matter / Google Home

ESP32の技術習得とMatterの学習のため、PC電源を Matter
 over Wi-Fiで操作するシステムを構築。

## About this Project

Ubuntu PCにGeneric ESP32-C3を統合し、スマートホーム規格「 **Matter **」に対応させるプロジェクトです。
Google Home / Nest Hubからの音声操作や自動化でPCの電源をON/OFFできます。
以前に行った案件のリベンジです。
PCの電源状態を他の家電と同様にシームレスに管理・操作することを目指しています。

## 機能

#### Step 1 — 電源制御

機能 手段 電源ON メカリレー → 電源ボタン短押し（500ms） 電源OFF メカリレー → 電源ボタン短押し（500ms）+ Ubuntu ACPI設定でシャットダウン ファクトリーリセット GPIO9 長押し（3秒） 
- **WoL（Wake on LAN）は不採用 **— このPCは設定したつもりでも、成功しなかった為 
- **ESP32ー ○○コマンド→PCで電源OFF **— そもそもPCを操作するのと変わらないため検討外 
- **電源OFF **: リレーで電源ボタンを短押しし、Ubuntuの ACPI
設定（ `HandlePowerKey=poweroff `）が正常シャットダウンを開始する 

#### Step 2 — 電源状態監視

機能 手段 電源状態検出 PC817 経由で電源 LED を GPIO 入力（アクティブLOW） 乖離検出 2秒ポーリング、3回連続で確定 Matter 属性同期 乖離確定時に `attribute::update() `で OnOff 属性を実態に合わせる ユーザー通知 Matter サブスクリプション経由（Google Home 等が自動受信） **フェイルセーフ原則 **: 乖離を検出してもシステムは自動での ON/OFF 操作を行わない。実態を Matter 属性に反映してユーザーへ委ねる。

## ハードウェア構成

#### 主要部品

- **マイコン **: Generic ESP32-C3 
- **ホストPC **: Ubuntu 
- **電源制御 **: シングルチャンネルリレーモジュール（ASIN: B0G4C9GMVH）でマザーボードの PWR SW ピンを短絡 
- **電源状態検出 **: PC817 フォトカプラ経由で電源 LED を読み取る 
- **コントローラー **: Google Nest Hub / Androidスマートフォン 
- **給電 **: PCのUSBポートからの常時給電 

#### GPIO 割り当て

GPIO 役割 回路 GPIO 20 OUTPUT: PWR SW制御 メカリレー経由 GPIO 4 INPUT: PWR LED検出 PC817 フォトカプラ経由（アクティブLOW） GPIO 9 INPUT: ファクトリーリセット 内部プルアップ、LOW=押下 

#### 回路図

**PWR SW（GPIO 20 → メカリレー → マザーボード） **

GPIO 20 → リレー制御入力
リレー接点 → マザーボード PWR SW ヘッダ短絡 **PWR LED（マザーボード → PC817 → GPIO 4） **

PWR_LED+ → 470Ω → PC817 Anode(pin1)
PC817 Cathode(pin2) → PWR_LED- (GND)
3.3V → 10kΩ → PC817 Collector(pin4) → GPIO 4
PC817 Emitter(pin3) → GND

PC ON : LED点灯 → PC817導通 → GPIO = LOW
PC OFF : LED消灯 → PC817遮断 → GPIO = HIGH (pullup) 極性は `pc_control.c `の `PWR_SW_ACTIVE_HIGH `ソースコードで切り替え可能。 


#### 主な材料費

部品 価格 Generic ESP32-C3 539円 リレーモジュール 464円 PC817 フォトカプラ 388円 **合計 ****1,391円 **
#### 待機電力（推測値）

機器 状態 推測消費電力 Generic ESP32-C3 Wi-Fi 常時接続・待機 約 0.3〜0.5W リレーモジュール 非作動時（コイル OFF） 約 0.01W 以下 フォトカプラ 非作動時 約 0.01W 以下 USBアダプタ損失 変換効率 80% 想定 +10〜20% **合計 ****約 0.4〜0.6W **上記は推測値。スマートフォン充電器の待機電力（0.1〜0.3W）と同程度であり、実用上は安心できるレベル。

## ソフトウェアスタック

レイヤー 名称 バージョン OS / SDK ESP-IDF 5.4.1 Matter ラッパー esp-matter `$ESP_MATTER_PATH `で指定 Matter 本体 ConnectedHomeIP (CHIP) esp-matter サブモジュール Matter デバイスタイプ: **On/Off Plug-in Unit **

## ビルド

#### WiFi 認証情報の設定

`main/wifi_creds.h `を作成してSSIDとパスワードを記載します（ `.gitignore `済み）: 


```
`#define WIFI_SSID     "your-ssid"
#define WIFI_PASSWORD "your-password" `
```

#### ビルド & フラッシュ


```
`. $IDF_PATH/export.sh
. $ESP_MATTER_PATH/export.sh
export _PW_ACTUAL_ENVIRONMENT_ROOT

idf.py set-target esp32c3
idf.py build
idf.py -p /dev/ttyACM0 flash `
```

#### Matter コミッショニング

フラッシュ後、シリアルモニタにQRコードとセットアップPINが出力されます。Google Home アプリ等でスキャンしてデバイスを登録してください。 

開発・テスト段階ではテスト用DAC（Device Attestation Certificate）を使用します。 

項目 値 Manual Pairing Code `34970112332 `Setup PIN `20202021 `Discriminator `3840 `

## 設計上の判断

#### BLE無効化・WiFiオンリーコミッショニング

`sdkconfig.defaults `で BLE を完全に無効化しています（ `CONFIG_BT_ENABLED=n `, `CONFIG_ENABLE_CHIPOBLE=n `）。 

**理由 **: `store_wifi_credentials() `でWiFi認証情報をハードコードしているため、デバイスは起動と同時にWiFi接続を試みます。
                    この状態でCHIPoBLE（MatterのBLEアドバタイズ）が動作すると、BLE/WiFi無線の競合によりWiFi接続が阻害される可能性があります。
                    WiFi認証情報を事前に埋め込む設計においては、BLEを無効化してIPネットワーク経由コミッショニング（ `kOnNetwork `）に統一しています。 


#### フェイルセーフ原則（乖離検出時の動作）

Matter 仕様の前提は「実態が確定的に判定できていること」。乖離時の自動 ON/OFF は誤動作リスクを生みます。 

安全な方向 = 操作しない。判断はユーザーに委ねる。 乖離確定（3回連続ポーリングで不一致）時の動作: 


1. `attribute::update() `で OnOff 属性を実態に同期 
2. Matter サブスクリプション経由でコントローラー（Google Home 等）へ通知 
3. 本システムは、得られた情報があっても電源を操作しない

## 既知の問題 / 課題

#### mDNS 競合（解消済み）

旧実装（Ping ベースの死活監視）では ESP-IDF `mdns_init() `と Matter 内部 mDNS がポート 5353 で競合していました。
                    現在は GPIO による電源 LED ポーリングに置き換えたため、mDNS は不使用。問題は解消済みです。 


#### フリーズ自動回復（未実装）

電源 LED が ON のまま PC が応答しない（フリーズ）ケースは、現状では検出していません。
                    手動対応が必要です。ユーザーはシステムを理解し、適切な対応を行う必要があります。

## 制限事項

- 本プロジェクトは自宅の一般的な家庭用ルーター環境を前提にしています。 
- 認証サーバーで厳重に管理されているネットワークや、セキュリティ管理が十分にされていないネットワークでは、
                        Matterの利用が制限される可能性があります。

## 補足
数週間つかっているとWifiの接続が悪くなりましたが原因不明。
Net情報では元々電波が弱いとの事。
アンテナを別途外だしできる基盤も売っていますので、実運用する場合はそちらを使用すべきかもしれません。
（値段が跳ね上がりますが）

## Resources

[View on GitHub](https://github.com/amekusa03/smarton-pc-c3)
