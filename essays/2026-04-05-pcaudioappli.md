# My PC Audio - Software Setup

2026/04/05 / Linux / Ubuntu

PCオーディオの操作を快適に

## Issues

現状のシステムではPCの前にいるときしか操作ができないことが課題です。

## Action

手元で操作する方法を模索しました。 

- PCのキーボードショートカットを活用する → 仰々しいので見送り 
- スマホから操作する方法を模索する → 採用 
PCをMusic Player Daemon (MPD)サーバーとして動かし、スマホ(Android)のアプリM.A.L.P.からWi-Fiを通じて選曲・操作する環境を構築します。 

```
`Android - M.A.L.P.で選曲・操作
        | WiFi  Cantata（PCのGUI）
        ↓         ↓
MPD（高音質再生エンジン） ポート: 6600
        ↓ PipeWire
ALC892 S/PDIF出力（カード1、デバイス1）
        ↓
TSS-1アンプ → スピーカー `
```

## Comparison of Components

Software Role Note **MPD **高音質再生エンジン 今回のメイン。バックグラウンドで動作。 **M.A.L.P. **スマホ用リモコン AndroidからWi-Fi経由で操作。 **Cantata **PC用クライアント PC上で操作したい場合に使用。

## Setup

PC (Ubuntu) に Music Player Daemon (MPD) をインストールします。 


### 1. 依存パッケージと権限の設定

```
`sudo apt update && sudo apt install ffmpeg -y `
```
MPDがユーザーディレクトリ内の音楽ファイルにアクセスできるよう、パーミッションを調整します。 


```
`chmod o+x /home/[username]
chmod o+rx "/home/[username]/ミュージック"
chmod o+rx "/home/[username]/ミュージック/公開" `
```

### 2. MPD のインストールと設定

```
`sudo apt install mpd mpc -y `
```

#### 設定のポイント

`~/.config/mpd/mpd.conf `を編集し、オーディオ出力を PipeWire に設定します。 


```
`audio_output {
    type        "pipewire"
    name        "PipeWire Output"
} `
```

#### 自動起動の設定


```
`# ユーザーサービスとして有効化
systemctl --user enable mpd
systemctl --user start mpd
# ログイン前からの自動起動を許可
sudo loginctl enable-linger [username] `
```

### 3. Android アプリ（M.A.L.P.）の設定


- **ホスト名: **Ubuntu の IP アドレス (例: 192.168.11.13) 
- **ポート: **6600 

### 4. PC用クライアント (Cantata) のインストール

PCのデスクトップから操作するためにインストールします。 


```
`sudo apt install cantata -y `
```

## Summary

これらのソフトウェアを組み合わせることで、PCオーディオ環境をスマホから操作できるようになりました。 


### Bonus

M.A.L.P.の操作は追加設定することなく、スマートウォッチからも可能でした。

## Figure

-

## Key Features

- **スマホからの操作: **M.A.L.P.を使用して、PCオーディオ環境をスマホから操作可能に。 
- **高音質再生: **MPDを使用して高音質なオーディオ再生を実現。

## Option

Navidromeをインストールしましたが、不要でした。 

インストール方法だけ、メモさせてください。 


### Navidrome のインストール


#### ffmpeg のインストール


```
`sudo apt update
sudo apt install ffmpeg -y `
```

#### Navidrome 本体のインストール

```
`wget https://github.com/navidrome/navidrome/releases/download/v0.61.0/navidrome_0.61.0_linux_amd64.deb
sudo apt install ./navidrome_0.61.0_linux_amd64.deb `
```

#### 設定ファイルの編集


```
`# /etc/navidrome/navidrome.toml
MusicFolder = "/home/[username]/ミュージック/公開" `
```

#### 音楽フォルダのアクセス権設定


```
`chmod o+x /home/[username]
chmod o+rx "/home/[username]/ミュージック"
chmod o+rx "/home/[username]/ミュージック/公開" `
```

#### サービスの起動


```
`sudo systemctl enable navidrome
sudo systemctl start navidrome `
```
