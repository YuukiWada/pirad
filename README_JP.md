# PiRAD

## 概要
PiRADはRaspberry Piを用いた放射線検出器です。安価でシンプルながら、X線・ガンマ線の光子毎の情報の取得 (エネルギーおよび到来時間) やMPPC用の高電圧の供給、MPPCの温度補償の機能などが利用できます。

本ソフトウェアおよび設計情報はGPL (GNU General Public License version3) ライセンスにて配布します。また本ソフトウェア・設計情報を使用して生じたいかなるトラブル・損失・損害に対して開発者は一切の責任を負いません。

## 使用方法
PiRADはRaspberry Piにスタックして使用するアナログ回路基板およびRaspberry Pi上で動作するソフトウェアより構成されています。

### 準備するもの
- Raspberry Pi 4B+ (メモリ容量は問わない)
- PiRAD基板
- MPPC・シンチレータ・同軸ケーブル
- 5V・2A以上のACアダプタ
- microSDカード (16GB以上のClass10を推奨)
- USBメモリ

### 回路基板
`circuit`ディレクトリにPCB基板を製造するのに必要なGerberファイルおよびパーツリストが格納されています。この情報を元にPCB基板の制作および部品の基板実装を実施してください。PCB基板は4層基板でサイズは105 mm×56 mmです。マウンター実装が可能なように捨て基板が設定されており、Vカットが必要です。またマウンター用基準マーカーも配置されています。

なおHV用のチップとしてLT3482IUDTRPBFが使用されています。このチップは部品の裏側に表面実装用のパッドがあることから、マウンター実装が必須になる可能性がありますので、ご注意ください。マウンター実装の場合は専用のメタルマスクを製造する必要があるため、初期費用がかかり、少数生産の場合は割高となります。少数生産の場合に有効な手法として、LT3482IUDTRPBFを未実装として製造し、のちほど手付けで実装する方法です。ただしヒートガンとソルダーペーストを用いて表面実装ができる技術を持っている場合に限ります。

### 放射線検出部
この部分は利用者の選択に委ねられています。作者のテスト環境ではMPPC (SiPM) に浜松ホトニクスS13360-6050CSを使用し、1×1×1 cmのGAGGシンチレータを取り付けています。回路基板に搭載されているHVは正極性ですので、カソードに電圧を供給し、アノードをGNDに接続します。作者の環境ではMPPCから回路基板まではSMA端子付きの同軸ケーブルで接続しています。

### データ取得ソフトウェア
`scripts`内にデータ取得ソフトウェアが格納されています。これらはC、Python、Rubyの3言語で構成されています。ソフトウェアの動作はRaspberry Pi4 Model BとRaspberry Pi OS with Desktop 32-bit brookwormにて確認しています。64-bit OSは動作対象外です。

ソフトウェアのセットアップ方法については`INSTALL_JP.md`を参照してください。

### 放射線データの取得
ソフトウェアの設定が終わったらUSBメモリに設定ファイルを書き込んでRaspberri Piに挿入します。設定ファイルの設定については`INSTALL_JP.md`を参照してください。

USBを挿入してRaspberry Piの電源を投入して暫く経つと、PWRのLEDが点灯します。点灯後に観測が開始可能となります。LOGGINGのスライドスイッチをONにすることでUSBメモリがマウントされ、観測が開始されます。USBメモリが読み込めない場合、LOGのLEDが2回点滅を繰り返します。

USBメモリが正常にマウントされ、パラメータファイルも正常に読み込めた場合、HV・LOGのLEDが点灯して計測が開始されます。放射線を検知した場合はRADのLEDが点滅します。

GPSモジュールを接続し、時刻同期設定をしている場合、GPSの捕捉によって時刻同期がされている間はGPSのLEDが点灯します。

計測を停止する場合はLOGGINGのスライドスイッチをOFFにします。数秒のうちにHV・LOGのLEDが消灯します。そのあとLOGのLEDが5回点滅するとUSBがアンマウントされ、Raspberry Piから安全に取り外しできるようになります。

シャットダウンする場合はPWR OFFスイッチをPWRのLEDが消灯するまで長押しします。このあとシャットダウン処理が完了するまで数分待ちます。シャットダウン処理を行わずに電源供給を停止した場合、SDカードの読み込み不良が起き、起動できなくなる可能性がありますので、注意してください。

### データフォーマット
データはUSBメモリ内に記録されます。放射線データはCSV形式のテキストで記録されており、計測開始時刻 (UTC) がファイル名となっています。ファイル内部は
```
1710139818.021942
0.000070, 410
0.395692, 73
1.175464, 88
1.209030, 88
1.948140, 94
2.283456, 67
2.334519, 144
```
のように記録されています。1行目は基準となる時刻 (UNIXTIME)、2行目以降は検出した放射線イベントに対応しており、1列目が基準時刻からの経過時間 (秒)、2列目が波高値です。波高値からエネルギーへの変換は放射線源などを用いたキャリブレーションが必要です。なおファイルは1日ごとに区切られ、UTCの0時 (日本時間の9時) 頃に切り替わります。

HK (housekeeping) データも同じく記録開始時刻をファイル名として保存されており、以下のように記録されています。

```
1706767240, 2024-02-01 06:00:40, 54.49946, 24.99, 30.12, 1011.96
1706767540, 2024-02-01 06:05:40, 54.49946, 24.83, 30.36, 1011.89
1706767840, 2024-02-01 06:10:40, 54.49946, 24.77, 30.31, 1011.87
1706768140, 2024-02-01 06:15:40, 54.49946, 24.91, 30.12, 1011.88
```
1列目はUNIXTIME、2列目は対応する時刻 (UTC)、3列目は実際に印加された高電圧の値、4列目は温度、5列目は湿度、6列目は大気圧となっています。なおHVの温度補償をOFFにしている場合 (温度センサーが接続されていない場合を含む) は温度以降のデータは記録されません。HKデータも同じくファイルは1日ごとに区切られ、UTCの0時 (日本時間の9時) 頃に切り替わります。

## 作成者情報
和田有希 (大阪大学 大学院工学研究科 電気電子情報通信工学専攻 助教)

## 更新情報
初版 2024年2月2日
第2版 2024年3月11日

