# My PC Audio - Software Setup

2026/04/05 / Linux / Ubuntu

Comfortable operation of PC audio

## Issues

The problem with the current system is that you can only operate it when you are in front of the PC.

## Action

I was looking for a way to operate it at hand. 

- Utilizing PC keyboard shortcuts → I decided not to do so because it seems pretentious 
- Looking for a way to operate from a smartphone → Recruitment 
We will run a PC as a Music Player Daemon (MPD) server and create an environment where you can select and operate songs from the M.A.L.P. app on your smartphone (Android) via Wi-Fi. 

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

Software Role Note **MPD **High-quality sound playback engine This time's main. Works in the background. **M.A.L.P. **Smartphone remote control Operated via Wi-Fi from Android. **Cantata **PC client Used when you want to operate on a PC.

## Setup

Install Music Player Daemon (MPD) on your PC (Ubuntu). 


### 1. Setting dependent packages and permissions

```
`sudo apt update && sudo apt install ffmpeg -y `
```
Adjust the permissions so that MPD can access the music files in your user directory. 


```
`chmod o+x /home/[username]
chmod o+rx "/home/[username]/ミュージック"
chmod o+rx "/home/[username]/ミュージック/公開" `
```

### 2. Installing and configuring MPD

```
`sudo apt install mpd mpc -y `
```

#### Setting points

Edit `~/.config/mpd/mpd.conf ` and set the audio output to PipeWire. 


```
`audio_output {
    type        "pipewire"
    name        "PipeWire Output"
} `
```

#### Automatic startup settings


```
`# ユーザーサービスとして有効化
systemctl --user enable mpd
systemctl --user start mpd
# ログイン前からの自動起動を許可
sudo loginctl enable-linger [username] `
```

### 3. Android app (M.A.L.P.) settings


- **Hostname: **Ubuntu IP address (e.g. 192.168.11.13) 
- **Port: **6600 

### 4. Installing the PC client (Cantata)

Install to operate from your PC desktop. 


```
`sudo apt install cantata -y `
```

## Summary

By combining these software, you can now control your PC audio environment from your smartphone. 


### Bonus

M.A.L.P. could be operated from a smartwatch without any additional settings.

## Figure

-

## Key Features

- **Operation from smartphone: **Using M.A.L.P., you can control your PC audio environment from your smartphone. 
- **High-quality audio playback: **Uses MPD to achieve high-quality audio playback.

## Option

I installed Navidrome, but it was unnecessary. 

Please let me know the installation method. 


### Installing Navidrome


#### Installing ffmpeg


```
`sudo apt update
sudo apt install ffmpeg -y `
```

#### Installing Navidrome

```
`wget https://github.com/navidrome/navidrome/releases/download/v0.61.0/navidrome_0.61.0_linux_amd64.deb
sudo apt install ./navidrome_0.61.0_linux_amd64.deb `
```

#### Editing the configuration file


```
`# /etc/navidrome/navidrome.toml
MusicFolder = "/home/[username]/ミュージック/公開" `
```

#### Music folder access rights settings


```
`chmod o+x /home/[username]
chmod o+rx "/home/[username]/ミュージック"
chmod o+rx "/home/[username]/ミュージック/公開" `
```

#### Starting the service


```
`sudo systemctl enable navidrome
sudo systemctl start navidrome `
```
