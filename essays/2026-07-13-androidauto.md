# Android Autoで取得可能な車両情報まとめ

OBD-IIを注文したけれど、なかなか納品されないのでAndroid Autoから取得できないか調べてみた。

2026-07-13 / Android Auto

## 基本的な車両情報 (CarInfo)

CarInfoでは、車両の静的な仕様や、動的なステータスを取得できる。

| カテゴリ | 取得できる情報 | 備考 |
| :--- | :--- | :--- |
| **車両モデル** | メーカー名 (Make)、モデル名 (Model)、年式 (Year) | `fetchModel()` |
| **エネルギー構成** | 燃料の種類（ガソリン、軽油等）、EVコネクタのタイプ | `fetchEnergyProfile()` |
| **燃料・バッテリー** | 燃料残量、バッテリー残量、燃料不足警告、推定航続距離 | `addEnergyLevelListener()` |
| **走行速度** | 実速度 (Raw Speed)、メーター表示速度 (Display Speed) | `addSpeedListener()` |
| **走行距離** | オドメーター（累計走行距離） | Android Autoで利用可能 |
| **ETC/有料道路** | 有料道路用カードの挿入状態、カードの種類 | `addTollListener()` |
| **外装寸法** | 車幅、車高、全長など | API Level 7以降 (主にAAOS) |

## センサー情報 (CarSensors)

CarSensorsでは、車両に搭載されている物理センサーの値を取得できる。

| カテゴリ | 取得できる情報 | 備考 |
| :--- | :--- | :--- |
| **加速度センサー (Accelerometer)** | 3軸の加速度データ。 |
| **ジャイロスコープ (Gyroscope)** | 3軸の回転速度データ。 |
| **コンパス (Compass)** | 車両の向き（方位）。 |
| **位置情報 (Location)** | 車両のGPSアンテナから取得した高精度な位置情報。スマホ側のGPSよりも精度が高い場合や、トンネル内での自律航法（Dead Reckoning）が効いたデータが得られる場合がある。 |

## 空調・クライアント設定 (CarClimate)

CarApp API Level 5以降で利用可能な比較的新しい機能。

| カテゴリ | 取得できる情報 |
| :--- | :--- |
| **HVAC (エアコン)** | ACのON/OFF、最大冷却 (Max AC)、内気循環の切り替え。 |
| **ファン** | 風量レベル、吹き出し方向。 |
| **温度設定** | 車内の設定温度。 |
| **デフロスター** | フロント/リアの曇り止め状態。 |

## 開発上の注意点

### 権限 (Permissions)

情報を取得するには、`AndroidManifest.xml` での宣言に加え、実行時にユーザーからの権限許可が必要。

* 例: `com.google.android.gms.permission.CAR_FUEL` (燃料情報)
* 例: `com.google.android.gms.permission.CAR_SPEED` (速度情報)

### 車両側の対応状況

全ての車両が全てのデータを提供しているわけではない。
データ取得時には必ず `CarValue.getStatus()` を確認し、`STATUS_SUCCESS` であることをチェックする必要がある。

### APIレベル

使用している Car App Library の API レベルによって、利用可能なメソッドが制限される場合がある（例：空調関係はレベル5以上）。

## 備考

スロットル開閉度とエンジン回転数は取得できず、ODB-IIの納品を待つしか無いとの結果。

## ソース

[https://developer.android.com/training/cars/apps/library?hl=ja](https://developer.android.com/training/cars/apps/library?hl=ja)
