# Android version of "Isekachi" character input problem, story of being killed by Gemini in seconds

2026.06.21
Android / Development notes

## discovery

One day, as I was typing on the Android version of ``Sekkachi'', something seemed strange. The cursor moves back and forth without permission, and entered characters disappear or are inserted in unknown locations. At first I thought it was the keyboard app's fault, so I tried changing a few things. However, the symptoms did not change.

## carving

The decisive blow came when I tried it in Google Chrome's search window. I was able to enter data there without any problems. It makes sense if you think about it, but if Chrome's search window was broken, the whole world would be in an uproar. That means it's an issue with the app. Confirmed due to "impatient" bug.

## solution

I opened Android Studio, but there are no clues. When I was at a loss, I threw the whole situation at Gemini.

The cause was quickly discovered.

```原因：
TextField の使い方の問題。IMEの未確定状態のままDBに保存し、それをそのまま再描画していた。
修正は「文字が確定してから保存する」というシンプルなもの。言われてみれば当たり前だが、ハマっているときはなかなか気づけない。
```

Incidentally
A sister app with the same structure, ``Lanch Memo,'' also had a similar problem, so we fixed it as well. Kill two birds with one stone.

---
Source: [github.com/amekusa03/androidSekkaTi](https://github.com/amekusa03/androidSekkaTi)
