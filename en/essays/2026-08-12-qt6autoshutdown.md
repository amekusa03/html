# Qt6(C++) AutoShutdown reimplementation

2026-08-12

## overview

A Qt application for Linux that detects idleness and automatically shuts down the system. It resides in the background of the system and automatically turns off the power to prevent unnecessary power consumption.

![Main Window](/en/essays/2026-08-12-qt6autoshutdown.png)

## background

It's been a while since I did Qt programming. AutoShutdown, which was previously created in Python, was rewritten in C++. I was concerned about library dependencies in the execution environment if I kept using the Python version, so I decided to rebuild it in C++.

## work

When creating a resident app, I first worried about what to do with the icon. After much thought, I asked AI to generate a simple and easy-to-understand icon.

It's been a while since I've used Qt6, so overall it took quite a while. In particular, I tried implementing C++ for screen operations this time.

## sauce

[Github view](https://github.com/amekusa03/qt6-desktop-autoshutdown)
