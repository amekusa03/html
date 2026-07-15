# Android不要アプリの整理方法（スクリプト編）

2026/05/17

古いスマホを快適に使えるようにしたいと思い、AndroidのプリインストールアプリをADBで削除することにした。その際、PowerShellスクリプトを使って削除ログを残しながら整理した。ここではその方法を解説する。

## このガイドについて

AndroidのプリインストールアプリをADBで削除する方法は、多くのサイトで紹介されている。しかし、削除したアプリをテキストファイルに記録しながら整理するPowerShellスクリプトを使った方法はあまり紹介されていない。ここでは、その使い方を解説する。

スクリプトを使うことで、次のメリットがある。 

- 何を消したか記録が残る 
- 複数アプリを続けて削除できる 
- ログを見ながら復元操作もできる

## 前提条件

このガイドを進める前に、以下が済んでいる必要があります。 

- PCに **ADB（SDK Platform-Tools） **がインストールされている 
- スマホの **開発者オプション **と **USBデバッグ **が有効になっている 
- USBケーブルでPCとスマホが接続されており、 `adb devices `でスマホが認識されている 
上記がまだの方は、 SDK Platform-Tools 公式ページ などを参照して準備してください。

## ステップ1：スクリプトを準備する

ADBを解凍したフォルダ（ `adb.exe `があるフォルダ）の中に、 `uninstall.ps1 `という名前でテキストファイルを作成し、以下の内容を貼り付けて保存します。 

```
`while ($true) {
    $pkg = Read-Host "パッケージ名を入力（終了はEnterのみ）"
    if ($pkg -eq "") { break }

    $result = adb shell pm uninstall -k --user 0 $pkg
    if ($result -match "Success") {
        $log = "$(Get-Date -Format 'yyyy/MM/dd HH:mm')  $pkg"
        Add-Content -Path "uninstalled_apps.txt" -Value $log
        Write-Host "削除完了：$pkg" -ForegroundColor Green
    } else {
        Write-Host "削除失敗：$result" -ForegroundColor Red
    }
} `
```

### スクリプトの動作

- パッケージ名の入力を繰り返し求めます 
- 削除が成功した場合、日時とパッケージ名を `uninstalled_apps.txt `に追記します 
- 削除に失敗した場合はエラー内容を表示します（ログには記録されません） 
- 何も入力せずEnterを押すと終了します

## ステップ2：スクリプトを実行する

1. ADBフォルダ内の何もない場所を「Shift＋右クリック」し、「PowerShellウィンドウをここで開く」を選びます。 
2. 以下のコマンドを入力してEnterを押します： 

```
`.\uninstall.ps1 `
```
「実行ポリシー」に関するエラーが出た場合は、先に以下を実行してから再試行してください。 


```
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned `
```

## ステップ3：パッケージ名を入力して削除する

スクリプトが起動すると「パッケージ名を入力」と表示されます。
                    削除したいアプリのパッケージ名（例： `com.example.app `）を入力してEnterを押してください。 

パッケージ名の調べ方： 


- **Android 8.0以上： **「設定」→「アプリ」→「すべてのアプリ」→ 対象アプリをタップして確認 
- **Android 7.x以下： **Google PlayからAplinをインストールして確認 
「削除完了：〇〇」と表示されれば成功です。続けて別のアプリを削除するか、Enterだけを押して終了します。

## ステップ4：ログファイルを確認する

削除が成功するたびに、ADBフォルダ内に `uninstalled_apps.txt `が自動で作られます。
内容は以下のような形式で記録されています。 


```
`2026/05/17 14:32  com.example.bloatware
2026/05/17 14:33  com.carrier.app `
```
このファイルを保管しておくことで、後で「何を消したか」をいつでも確認できます。

## 参考：AQUOS向け削除候補パッケージ

AQUOS（シャープ製Android）を使っている場合の参考情報です。機種やAndroidバージョンによって存在しないパッケージもあります。 


### シャープ独自機能（使わないなら無効化候補）

AQUOS特有の機能です。使っていなければ削除候補になります。 

パッケージ名 機能 `jp.co.sharp.android.emopar `エモパー（AIアシスタント） `jp.co.sharp.android.emopa.systemservice ``jp.co.sharp.android.launcherguide `操作ガイド `jp.co.sharp.android.shtutorialapp `チュートリアル `jp.co.sharp.android.pedometer.framework.server `歩数計 `jp.co.sharp.android.pedometersettingapp ``jp.co.sharp.android.karadamate `からだメイト `jp.co.sharp.android.scrollauto `スクロールオート `jp.co.sharp.android.paytriggerw `Payトリガー（指紋センサーで決済アプリ起動） 

### Google系アプリ（代用アプリがあるなら）

パッケージ名 機能 `com.google.android.apps.fitness `Google Fit `com.google.android.apps.magazines `Google ニュース `com.google.android.apps.books `Google Play ブックス `com.google.android.apps.bard `Google Gemini / Bard `com.google.chromeremotedesktop `リモートデスクトップ 

### ⚠️ 触ってはいけないパッケージ

以下は削除するとスマホが正常に動かなくなる（最悪、起動しなくなる）可能性があります。絶対に消さないでください。 

パッケージ名 役割 `android `システム根幹 `jp.co.sharp.android.launcher3 `ホーム画面 `com.android.systemui `通知・画面表示 `com.felicanetworks.* `おサイフケータイ機能 `com.mediatek.* `CPU・通信チップの制御 `jp.co.sharp.overlay.*`画面表示の調整用データ

## 削除したアプリを元に戻す方法

ログファイルに記録されたパッケージ名を使って、削除したアプリを復元できます（Android 7.0以上）。
PowerShellで以下のコマンドを実行してください。 

```bash
`adb shell cmd package install-existing パッケージ名 `
```

「Success」と表示されれば復元完了です。 
※Android 7.0未満では復元できません。削除前に慎重に判断してください。

## まとめ

スクリプトを使うことで、コマンドを毎回手打ちする手間が省け、削除したアプリの記録も自動で残せます。
ログファイルがあれば「あのアプリ消したっけ？」という不安もなくなります。 

スマホの整理に役立てば嬉しいです。
