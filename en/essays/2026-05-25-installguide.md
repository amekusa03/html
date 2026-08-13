# How to install Android apps

2026/05/25 / kotlin

Steps to run GitHub source code on a smartphone

## Introduction

We will summarize how to use Android apps published on GitHub on your smartphone.
Even if you have no experience developing apps, you can install it on your smartphone using Android Studio by following the steps.
This guide provides easy-to-understand explanations from environment construction to transfer to the actual device.

## Step 1: Install Android Studio

First, install the development tool "Android Studio" on your computer.

1. Access [Android Studio official website](https://developer.android.com/studio).
2. Click the "Download Android Studio" button, agree to the terms, and download the installer.
3. Run the downloaded file and basically click "Next" to complete the installation.
4. Several components are downloaded on first startup. Please wait as it will take some time.

## Step 2: Get the code from GitHub

Next, download the program (source code) of the app you want to run.

1. Open the GitHub project page (e.g. [WebLauncher2](https://github.com/amekusa03/WebLauncher2) ).
2. Click the green "< > Code" button and select "Download ZIP".
3. Extract (unzip) the downloaded ZIP file to a location of your choice (desktop, etc.) on your computer.

## Step 3: Open the project in Android Studio

1. Start Android Studio and select "Open".
2. Select and open the folder you just extracted (look for the folder with the Android icon).
3. "Gradle Sync" will start at the bottom right. It will automatically collect the necessary libraries, etc., so wait a few minutes until it finishes (until the bar disappears).

## Step 4: Preparing the smartphone side (developer option)

To send the app to your smartphone, you need to enable "debug mode" on your smartphone.

1. Open your smartphone's "Settings" → "Device information".
2. Tap "Build number" 7 times in a row. "You are now a developer" will be displayed.
3. Open "Settings" → "System" → "Developer Options" and turn on **USB Debugging**.
4. Connect your smartphone and computer with a USB cable. When asked “Do you want to allow USB debugging?” press OK.

## Step 5: Install on smartphone

1. Make sure that the name of your smartphone is displayed in the device selection field at the top of Android Studio.
2. Click the green play button (Run 'app') to the right of it.
3. The program will begin to build, and if successful, the app will automatically launch on your smartphone.
**Note:** If an error occurs during the build, the version of Android Studio may be old or the OS version of your smartphone may not be compatible.

## summary

Once you create an environment, you can try out other GitHub projects using the same steps.
Even just looking at the source code and slightly changing the numbers and colors can be the first step in app development. Please enjoy it!
