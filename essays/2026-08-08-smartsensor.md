# ワンコインで作る、我が家の「空模様センサー」

## 概要

CdSセル（光導電素子）一つで、Google Home 連携の照度センサーを作ってしまおう、という工作です。部品代は合計でも500円しないくらい。ESP32-C6 に Matter ファームウェアを書き込んで、家の照明の自動点灯ロジックに天候の影響を織り込みました。

![Google Homeアプリでの照度センサー](<essays/2026-08-08-smartsensor.png>)

### 部品

|部品名|価格|型番|
|:---|:---|:---|
|ESP32-C6|449円|Generic-RP030MERU6D5SHUL4A|
|CdSセル|40円|GL5528等の標準光導電素子|
|10kΩ抵抗|1円|100本入り100円|

### アプリ概要

ESP32-C3 を用いた Matter 対応照度センサー（Ambient Light Sensor）ファームウェアです。CdSセル（光導電素子）と固定抵抗による分圧回路の電圧を ADC で取得し、照度（Lux）に変換したうえで、Matter 規格の `IlluminanceMeasurement` 属性（`MeasuredValue`）としてネットワーク上に提供します。

### 接続表（Pin Mapping）

| ESP32-C6 ピン | 接続先 | 役割 |
| :--- | :--- | :--- |
| **3.3V** | CdSセルの片足 | 電源供給 |
| **GPIO1（ADC1_CH1）** | CdSセルと10kΩ抵抗の接続点 | ADC電圧計測入力 |
| **GND** | 10kΩ抵抗の片足 | グランド |

## 経緯

何か工作したいなぁ、と部品をあさっていると、CdSセルを発見。そう言えば最近は天候不順続きで、日没時刻に合わせて自動点灯させていた照明が、曇りや雨の日はまだ明るいうちに点いてしまったり、逆に暗くなっても点かなかったりして、結局は手動でオン・オフしていたことを思い出しました。

だったら、時刻ではなく「実際の明るさ」で判断させればいい。CdSセルでGoogle Homeの光センサーを自作しよう、と思い立ったのが今回のきっかけです。

## 作業工程

1. CdSセルをサーキットテスターで測定し、光量によって抵抗値が変わることを確認。新品とはいえ、10年以上は部品箱に埋蔵されていたものを発掘したものなので、まずは生きているかどうかの確認から。
2. CdSセルと10kΩ抵抗で分圧回路を組む。
3. ESP32-C3のADC1_CH1ピンに、分圧回路の出力を接続。
4. ESP32-C3にMatterテスト用の照度センサーファームウェアを書き込み、実測値との照らし合わせでおおまかにLux値を算定。
5. Google Home用にファームウェアを作成。以前行ったPCのMatter化のコードをベースに、センサー関連部分を修正。
6. Google Homeに照度センサーを登録。
7. スマートフォンで照度センサーの値を表示確認。
8. Google HomeにYAMLで自動化ロジックを追加。

```yaml
metadata:
  name: 暗くなったら照明をつける
  description: 16:00~20:00に50lux以下となったら、照明を点灯し、「暗くなりました」と言います。
automations:
  - starters:
      - type: device.state.SensorState
        device: 光量 - リビングルーム
        # センサーの種類（LightLevel 等）の指定形式はデバイスによって異なる場合があります
        state: currentSensorStateData.LightLevel.rawValue
        lessThanOrEqualTo: 50
    condition:
      type: time.between
      after: 16:00
      before: 20:00
    actions:
      - type: device.command.OnOff
        devices:
          - ライト - リビングルーム
        on: true
      - type: assistant.command.Broadcast
        message: "暗くなりました"
```

## 総評

数時間で大きなトラブルもなく完成してしまいました。あえて反省点を挙げるなら、ハンダ付けの最中にV3.3とP3のピンを間違えたこと。再発防止策として、回路図メモには「3.3」ではなく「V3.3」のように単位まで書くこと、そして何より、老眼鏡はちゃんとかけること👓😅

## ソース

[GitHub Repository](https://github.com/amekusa03/smartOptSensor)