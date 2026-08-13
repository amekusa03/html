# AutoShutdown — automatic shutdown during inactivity

2026/05/28 / python/ubuntu

I took a nap with the PC on and decided to use the economy version of Ubuntu.

## overview

A small utility that detects inactivity in X11/Wayland environments and shuts down after a specified time.
This is a program on Ubuntu that automatically shuts down if there is no mouse or keyboard operation for a certain period of time. It prioritizes X11 idle detection and also has a fallback via `gdbus` on GNOME/Wayland.

## function

- Accurate inactivity detection using X11's idle detection
- `gdbus` fallback in GNOME/Wayland environment
- Configurable inactivity time (default 5 minutes)
- Automatic start as systemd user service
- Operation can be monitored with log files
- 1 minute notice time before shutdown

## install

```bash
cd /home/kusa/ドキュメント/AutoShutdown
bash install.sh
```

Running the installation script installs dependencies and registers the systemd service. Please check the contents of the script in advance.

## setting

The settings are done in `config.ini` (example):

```ini
[general]
idle_timeout = 300      # 無操作時間（秒）
check_interval = 10     # チェック間隔（秒）
enabled = true
```

Please restart the service after changing the settings.

```bash
systemctl --user restart auto-shutdown
```

## How to use

Example of service operation:

```bash
# 起動
systemctl --user start auto-shutdown

# 停止
systemctl --user stop auto-shutdown

# ステータス確認
systemctl --user status auto-shutdown

# ログ（リアルタイム）
journalctl --user -u auto-shutdown -f
```

Manual execution:

```bash
python3 /home/kusa/ドキュメント/AutoShutdown/auto_shutdown.py
```

## troubleshooting

### xprintidle not found

```bash
sudo apt install xprintidle libglib2.0-bin
```

Idle detection in Wayland environment is done via gdbus. Operation confirmation command:

```bash
gdbus call --session --dest org.gnome.Mutter.IdleMonitor \
  --object-path /org/gnome/Mutter/IdleMonitor/Core \
  --method org.gnome.Mutter.IdleMonitor.GetIdletime
```

## uninstall

```bash
systemctl --user stop auto-shutdown
systemctl --user disable auto-shutdown
sudo rm /etc/sudoers.d/autoshutdown
```

## Resource

[https://github.com/amekusa03/AutoShutdown](https://github.com/amekusa03/AutoShutdown)
