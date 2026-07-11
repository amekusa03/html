# AntigravityのVersionUp

2026.07.10
Google Antigravity

## 更新の通知

Antigravity 1.23.2 Ubuntu版を使用していると更新通知があったので、早速更新する事にした。

## Antigravityの分離

サイトに行くと、AntigravityとAntigravity IDEの二つのファイルがある。
どうやら、今回からAntigravity IDEとAntigravity本体とで分かれたようです。
IDEはGUI版で、CLI版もあるようですが、私はIDE版をインストール（アップデート）します。

## まさかのtar.gz

サイトに行くとupdateコマンドはなく、ダウンロード形式。
tar.gz形式でダウンロードし、解凍してとりあえず動かすと動く。
ということは、その他の設定ファイルは自分で用意しないといけないのか。

## Setup

- とりあえず、既存削除

```bash
sudo rm -rf /opt/antigravity-ide
```

- 解凍して、設置（IDEの前に空白あるし）

```bash
tar -xzf ~/Downloads/"Antigravity IDE.tar.gz"
sudo mv "antigravity ide" /opt/antigravity-ide
```

- アプリケーションメニューの設定ファイル作成

```bash
touch ~/.local/share/applications/antigravity-ide.desktop
```

- アイコン探しの終着点

/opt/antigravity-ide/resources/app/resources/linux/code.png

- ファイルの中身

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

(2026/07/11 Execに%Fを追加)

## え

実行すると久しぶりのコアダンプ。

[33309:0709/164822.174543:FATAL:sandbox/linux/suid/client/setuid_sandbox_host.cc:166] The SUID sandbox helper binary was found, but is not configured correctly. Rather than run without sandboxing I'm aborting now. You need to make sure that /opt/antigravity-ide/chrome-sandbox is owned by root and has mode 4755.
Trace/breakpoint trap (コアダンプ)

## 蘇生

ネット情報ではサンドボックスの実行権限がNGらしい。

1. ファイルの所有者を root ユーザーに変更します

```bash
sudo chown root:root /opt/antigravity-ide/chrome-sandbox
```

1. 権限を「4755」（SUIDビットを立てる）に設定します

```bash
sudo chmod 4755 /opt/antigravity-ide/chrome-sandbox
```

## 起動できましたが

~~まだ、関連ファイルからの起動ができない。
これはまた追って調査します。~~
(2026年7月11日追記)

- ケアレスミスでした。antigravity-ide.desktopのExecの最後に%Fが抜けていただけでした。

## ソース

[https://antigravity.google/](https://antigravity.google/)
