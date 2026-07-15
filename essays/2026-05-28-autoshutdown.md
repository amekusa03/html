# AutoShutdown — 無操作時の自動シャットダウン

2026/05/28 / python/ubuntu

PCの電源をつけたままうたた寝し、エコノミーな、Ubuntuにしよと思いました。

## 概要

X11/Wayland環境で無操作を検出し、指定時間後にシャットダウンする小さなユーティリティ。
Ubuntu上で、マウスやキーボードの操作が一定時間ない場合に自動的にシャットダウンするプログラムです。X11のアイドル検出を優先し、GNOME/Waylandでは `gdbus` 経由のフォールバックも行います。

## 機能

- X11のアイドル検出を使用した正確な無操作検出 
- GNOME/Wayland環境での `gdbus` フォールバック 
- 設定可能な無操作時間（デフォルト5分） 
- systemdユーザーサービスとして自動起動 
- ログファイルで動作を監視可能 
- シャットダウン前に1分の予告時間

## インストール

```
cd /home/kusa/ドキュメント/AutoShutdown
bash install.sh
```
インストールスクリプトを実行すると、依存関係のインストールと systemd サービスの登録が行われます。スクリプトの内容を事前に確認してください。

## 設定

設定は `config.ini `で行います（例）: 


```
[general]
idle_timeout = 300      # 無操作時間（秒）
check_interval = 10     # チェック間隔（秒）
enabled = true
```

設定変更後はサービスを再起動してください。

```
systemctl --user restart auto-shutdown
```

## 使用方法

サービス操作の例： 


```
# 起動
systemctl --user start auto-shutdown

# 停止
systemctl --user stop auto-shutdown

# ステータス確認
systemctl --user status auto-shutdown

# ログ（リアルタイム）
journalctl --user -u auto-shutdown -f `
```
手動実行： 


```
`python3 /home/kusa/ドキュメント/AutoShutdown/auto_shutdown.py `
```

## トラブルシューティング

### xprintidleが見つからない


```
`sudo apt install xprintidle libglib2.0-bin `
```
Wayland環境でのアイドル検出は gdbus 経由で行います。動作確認コマンド： 


```
gdbus call --session --dest org.gnome.Mutter.IdleMonitor \
  --object-path /org/gnome/Mutter/IdleMonitor/Core \
  --method org.gnome.Mutter.IdleMonitor.GetIdletime
```

## アンインストール

```
`systemctl --user stop auto-shutdown
systemctl --user disable auto-shutdown
sudo rm /etc/sudoers.d/autoshutdown `
```
## Resource

https://github.com/amekusa03/AutoShutdown
