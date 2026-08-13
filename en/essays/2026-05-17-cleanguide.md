# How to organize Android unnecessary apps (script edition)

2026/05/17

I wanted to be able to use my old smartphone more comfortably, so I decided to delete pre-installed Android apps using ADB. At that time, I used a PowerShell script to organize while leaving a deletion log. Here we will explain how.

## About this guide

Many sites introduce how to delete preinstalled Android apps using ADB. However, there is not much introduction to how to use a PowerShell script to organize deleted apps while recording them in a text file. Here we will explain how to use it.

Using scripts has the following advantages: 

- A record of what was deleted remains 
- You can delete multiple apps in succession 
- You can also perform restore operations while viewing the logs.

## Prerequisites

Before proceeding with this guide, you must have: 

- **ADB (SDK Platform-Tools)** is installed on the PC 
- Your phone's **Developer options** and **USB debugging** are enabled. 
- The PC and smartphone are connected with a USB cable, and the smartphone is recognized by `adb devices ` 
If you have not done the above yet, please refer to the SDK Platform-Tools official page and prepare.

## Step 1: Prepare the script

Create a text file named `uninstall.ps1 ` in the folder where you unzipped ADB (the folder containing `adb.exe `), paste the following content, and save it. 

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

### Script behavior

- Prompts repeatedly for package name 
- If the deletion is successful, add the date, time and package name to `uninstalled_apps.txt ` 
- If deletion fails, the error details will be displayed (not recorded in the log) 
- Press Enter without entering anything to exit.

## Step 2: Run the script

1. ``Shift + right-click'' an empty space in the ADB folder and select ``Open PowerShell window here.'' 
2. Type the command below and press Enter: 

```
`.\uninstall.ps1 `
```
If you receive an error related to "execution policy", please do the following first and then try again. 


```
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned `
```

## Step 3: Enter package name and delete

When the script starts, it will ask you to enter the package name.
                    Enter the package name of the app you want to remove (e.g. `com.example.app `) and press Enter. 

How to find the package name: 


- **Android 8.0 or higher: **"Settings" → "Apps" → "All apps" → Tap the target app to confirm 
- **Android 7.x and below: **Install Aplin from Google Play and check 
If "Delete completed: 〇〇" is displayed, it is successful. Continue to remove another app or just press Enter to exit.

## Step 4: Check the log file

`uninstalled_apps.txt ` is automatically created in the ADB folder every time the deletion is successful.
The contents are recorded in the following format. 


```
`2026/05/17 14:32  com.example.bloatware
2026/05/17 14:33  com.carrier.app `
```
By saving this file, you can always check what you deleted later.

## Reference: Removal candidate package for AQUOS

This is reference information when using AQUOS (Sharp Android). Some packages may not exist depending on the model or Android version. 


### Sharp's unique features (candidates for disabling if not used)

This is a feature unique to AQUOS. If you are not using it, it will be a candidate for deletion. 

Package Name Function `jp.co.sharp.android.emopar `Emopa (AI assistant) `jp.co.sharp.android.emopa.systemservice ``jp.co.sharp.android.launcherguide `Operation guide `jp.co.sharp.android.shtutorialapp `Tutorial `jp.co.sharp.android.pedometer.framework.server `Pedometer `jp.co.sharp.android.pedometersettingapp ``jp.co.sharp.android.karadamate `Karada Mate `jp.co.sharp.android.scrollauto `Scroll auto `jp.co.sharp.android.paytriggerw `Pay trigger (launch payment app with fingerprint sensor) 

### Google apps (if there are alternative apps)

Package Name Features `com.google.android.apps.fitness `Google Fit `com.google.android.apps.magazines `Google News `com.google.android.apps.books `Google Play Books `com.google.android.apps.bard `Google Gemini / Bard `com.google.chromeremotedesktop `Remote Desktop 

### ⚠️ Packages that should not be touched

If you delete the following, your smartphone may not work properly (or in the worst case, it may not start up). Please never delete it. 

Package name Role `android `System core `jp.co.sharp.android.launcher3 `Home screen `com.android.systemui `Notification/screen display `com.felicanetworks.* `Osaifu-Keitai function `com.mediatek.* `CPU/communication chip control `jp.co.sharp.overlay.*`Data for adjusting screen display

## How to restore deleted apps

You can restore deleted apps using the package name recorded in the log file (Android 7.0 and above).
Execute the following command in PowerShell. 

```bash
`adb shell cmd package install-existing パッケージ名 `
```

If "Success" is displayed, the restoration is complete. 
*Restore is not possible on Android versions lower than 7.0. Please think carefully before deleting.

## summary

By using a script, you can save yourself the trouble of entering commands manually each time, and you can also automatically keep a record of deleted apps.
If you have a log file, you won't have to worry about "Did I delete that app?" 

I hope this helps you organize your smartphone.
