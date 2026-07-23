# Google Nest Hub で PC 電源を操作

2026/07/24 / ESP-IDF / Matter / Google Home

PC電源を Google Nest Hub で操作するシステムを構築。
本バージョンでは**専用配線を完全廃止**しました。
副産物としてOSも問いません。

## 概要

PCにGeneric ESP32-C6を統合し、スマートホーム規格「Matter」に対応させた。
Google Home / Nest Hubからの音声操作や自動化でPCの電源をONできます。
PCの電源状態を他の家電と同様にシームレスに管理・操作することを目指しています。

## 注意事項

- 電源のONは可能ですが、OFF機能はありません。

## 主な特徴

- **Windows / Ubuntu 両対応**: USBとWOLの組み合わせによりWindows/Ubuntu両OSで利用可能。
- **専用配線の完全廃止**: メカリレーやフォトカプラ等のマザーボード配線は一切不要。PC の USB ポートに挿すだけで導入可能。
- **Wake-on-LAN (WOL) リモート起動**: Matter から ON 操作を受信した際、設定された MAC アドレス宛てに Wake-on-LAN マジックパケットを送信して PC を起動。
- **USB 通信状態ベースの PC 監視**: 2秒周期で USB Serial/JTAG 接続状態（`usb_serial_jtag_is_connected()`）を監視し、PC の実際の電源状態（ON / OFF）を判定。
- **Matter 属性自動同期 & フェイルセーフ**: PC の実際の電源状態と Matter 属性値の乖離を検出した際、誤操作防止の安全ガード（`s_syncing_attribute`）付きで Matter 属性を自動更新・自動同期。
- **ST7789 カラー LCD リアルタイム表示**: Wi-Fi 接続状態、割り当て IP アドレス、PC 状態（ON / OFF / BOOTING）、動作ステータスログをグラフィカルに表示。
- **省電力＆画面保護（5分自動消灯）**: PC が `OFF` になってから 5 分経過すると LCD バックライト（輝度）を自動で `0`（消灯）に移行。PC が起動・復帰すると即座に自動点灯。
- **Google Home 互換性最適化**:
  - Wi-Fi 省電力モード無効化（`WIFI_PS_NONE`）による IPv6 mDNS（`_matter._tcp`）ドロップ防止。
  - MAC アドレスベースの決定論的 UniqueID（`chip-config/unique-id`）自動生成。

## 設定事項

- PCのWOL設定、BIOSの設定でPCのUSBの給電設定を常にONになるように設定する
- ESP32-C6のWi-Fi設定を `main/wifi_creds.h` に記述する

## ハードウェア仕様

- **マイコンボード**: Waveshare ESP32-C6-GEEK
- **ディスプレイ**: 1.14 インチ ST7789 カラー LCD (240 × 135)
- **接続方式**: USB Type-A 接続（PC の USB ポート）
- **物理配線**: なし（USB 給電および接続検知）
- **リセットボタン**: GPIO 9 (BOOT ボタン長押し 3 秒で Factory Reset)

---

## ソフトウェアスタック

| レイヤー | 名称 | バージョン / 設定 |
|---------|------|------------------|
| OS / SDK | ESP-IDF | v5.4.1 |
| ターゲット | ESP32-C6 | `esp32c6` |
| スマートホーム規格 | esp-matter / Matter | Wi-Fi (`kOnNetwork`) |
| デバイスタイプ | On/Off Plug-in Unit | Cluster: `0x0006` (OnOff) |
| 電源制御方式 | Wake-on-LAN (WOL) | UDP Port 9 / Magic Packet |

## ネットワーク設定

セキュリティ上の理由により、SSID やパスワード、MAC アドレス等の認証情報は Git 管理対象外（`.gitignore` に登録）となっています。  
初回ビルド前に `main/wifi_creds.h` を新規作成し、お使いの環境に合わせて以下の内容を設定してください。

## Resources

[View on GitHub](https://github.com/amekusa03/smarton-pc-c6)
