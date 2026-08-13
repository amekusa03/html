# Antigravity Version Up

2026.07.10
Google Antigravity

## Update notification

When I was using Antigravity 1.23.2 Ubuntu version, I received an update notification, so I decided to update it immediately.

## Antigravity separation

When you go to the site, you will see two files: Antigravity and Antigravity IDE.
Apparently, from this time onwards, Antigravity IDE and Antigravity itself have been separated.
The IDE is a GUI version, and there seems to be a CLI version as well, but I will install (update) the IDE version.

## Unexpected tar.gz

When you go to the site, there is no update command, but a download format.
Download it in tar.gz format, unzip it, and run it for now.
Does that mean I have to prepare other configuration files myself?

## Setup

- For now, delete the existing

```bash
sudo rm -rf /opt/antigravity-ide
```

- Unzip and install (there is a blank space before the IDE)

```bash
tar -xzf ~/Downloads/"Antigravity IDE.tar.gz"
sudo mv "antigravity ide" /opt/antigravity-ide
```

- Creating a settings file for the application menu

```bash
touch ~/.local/share/applications/antigravity-ide.desktop
```

- The end point of your search for icons

/opt/antigravity-ide/resources/app/resources/linux/code.png

- Contents of the file

```bash
[Desktop Entry]
Version=1.0
Type=Application
Name=Antigravity IDE
Comment=Antigravity IDE Editor
Exec=/opt/antigravity-ide/antigravity-ide %F
Icon=/opt/antigravity-ide/resources/app/resources/linux/code.png
Terminal=false
Categories=Development;IDE;
```

(2026/07/11 Added %F to Exec)

## picture

When I run it, it dumps core for the first time in a while.

[33309:0709/164822.174543:FATAL:sandbox/linux/suid/client/setuid_sandbox_host.cc:166] The SUID sandbox helper binary was found, but is not configured correctly. Rather than run without sandboxing I'm aborting now. You need to make sure that /opt/antigravity-ide/chrome-sandbox is owned by root and has mode 4755.
Trace/breakpoint trap (core dump)

## resuscitation

According to the information on the internet, the sandbox execution privilege is NG.

1. Change the file owner to root user

```bash
sudo chown root:root /opt/antigravity-ide/chrome-sandbox
```

1. Set permissions to "4755" (set SUID bit)

```bash
sudo chmod 4755 /opt/antigravity-ide/chrome-sandbox
```

## I was able to start it, but

~~Still unable to start from related files.
I will investigate this further. ~~
(Added on July 11, 2026)

- It was a careless mistake. The only thing missing was %F at the end of Exec in antigravity-ide.desktop.

## sauce

[https://antigravity.google/](https://antigravity.google/)
