# PiRAD ソフトウェアインストール方法

## 概要
本ページではPiRADで使用するRaspberry Pi用のソフトウェアのインストール方法を記述しています。なお本ソフトウェアはRaspberry Pi 4B+での動作を前提としており、他のRaspberry Piのバージョンでは動作確認を行っていません。またSSHでRaspberry Piにアクセスできる環境を前提としています。

## 準備するもの
- Raspberry Pi 4B+
- microSDカード (16GB以上のClass10を推奨)
- Raspberry Pi用の電源
- USBメモリー (FAT32でフォーマット)
- 設定用のPC (作者はmacOSを使用)

## インストールの手順

### SDカードの準備
まずSDカードにRaspberry Pi用のOSを書き込みます。書き込みにはRaspberry Pi Imagerを用います。[こちら](https://www.raspberrypi.com/software/) から対応するソフトウェアをダウンロードしてインストールします。

SDカードをPCに挿入して、Raspberry Pi ImagerでOSを書き込みます。Raspberry Pi DeviceはRaspberry Pi 4、OSはRaspberry Pi OS (32-bit) Debian Bookworm with the Raspberry Pi Desktopを選択します。<span style="color: red;">かならず32-bitを選択してください。</span>

![Raspberry Pi Imager](images/imager.png)

書き込み先のSDカードを選択したあと、OSのカスタマイズについて聞かれるので、「設定を変更する」を選択します。設定画面でユーザー名とパスワードを設定します。ユーザー名はここではpiとします。サービスのタブで「SSHを有効化する」にチェックを入れてください。設定が終わったら書き込みを開始します。

### OSの準備
書き込みが終わったSDカードをRaspberry Piに差し込ます。有線LANでネットワークに接続されていることを確認し、Raspberry Piに電源を供給します。ルーター等でRaspberry Piに割り当てられたIPアドレスを確認します。

SSHでRaspberry Piにアクセスします。コマンド例は
```
ssh pi@192.168.1.2
```
です。ユーザー名やIPアドレスはそれぞれの設定環境で異なります。

続いてGPIOの設定を行います。
```
sudo raspi-config
```
と入力して設定画面を開きます。"Interface Options"を選択し、SPI、I2C、Serial Portを有効化しておきます。またこのとき必要であれば、タイムゾーンなども変更しておくとよいでしょう。タイムゾーンは初期設定ではGMTとなっています。

必須ではないものの、公開鍵認証を導入しておくとよいでしょう。
```
mkdir ~/.ssh
cd ~/.ssh/
nano authorized_keys
```
として、`authorized_keys`に公開鍵を記入しておくと、次回からパスワード入力なしでログインできるようになります。

### ソフトウェアのクローンとインストール
まずGitHubからソースコードをクローンします。
```
mkdir ~/git
cd ~/git
git clone https://github.com/YuukiWada/pirad
cd pirad
```

まずDAQソフトウェアをコンパイルします。
```
cd ~/git/pirad/scripts/c_lang
bash ./make.sh
```
特にエラーメッセージが表示されなければ、コンパイルは成功しています。

続いてスクリプトの動作に必要なソフトウェアをインストールします。
```
sudo apt install -y ruby ruby-dev openssl libssl-dev
sudo apt install -y python3-smbus python3-smbus2 python3-bme280 python3-yaml
```

さらにcrontabの設定を行います。
```
~/git/pirad/scripts/crontab_setting.txt
```
の内容を
```
sudo crontab -e
```
でcrontabの編集画面上に追記します。ここまでできたら
```
sudo reboot
```
で再起動します。設定がうまくいくと、再起動後にPWRのLEDが点灯します。

### USBメモリーの準備
PiRADは日常的に使用する際に、Raspberry Piにアクセスする必要がないよう、設定ファイルをUSBメモリーから読み出し、まだ観測データもUSBメモリーに直接書き込んでいます。USBメモリはFAT32でフォーマットしておいてください。

USBメモリーのトップディレクトリに[config.yaml](https://github.com/YuukiWada/pirad/blob/main/scripts/config.yaml)を格納してください。内容は
```
hv: 56.0
threshold: 10
compensation: off
temp_const: 0.054
hv_limit: 60
```
となっています。上からHVの設定値、DAQのスレッショルド、MPPCに供給する高電圧の温度補償の有無、MPPCの温度係数 [V/degC]、HVの上限値が記載されています。温度センサーが取り付けられていない場合はcompensationはoffにしてください。

設定ファイルを書き込んだUSBメモリーをRaspberry Piに挿してください。USBメモリーがUSB3.0に対応している場合は、USB3.0のポートに挿すことを推奨します。

LOGGINGのスイッチをONにして数秒待つと、HVのLED、続いてLOGのLEDが点灯し、放射線が観測されるとRADのLEDが点滅します。

### GPSによる時刻同期の設定
GPSモジュールを接続している場合、オフラインでもGPSによる時刻同期が可能となります。

```
sudo nano /boot/cmdline.txt
```
として記載されている行を#でコメントアウトし、代わりに
```
dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline rootwait
```
と入力します。続いて
```
sudo nano /boot/config.txt
```
として、最後の行に
```
init_uart_baud=9600
dtoverlay=pps-gpio,gpiopin=4,assert_falling_edge=true
```
と記入します。assert_falling_edgeは使用するGPSモジュールによって異なり、PPSがたち下がりパルス (アクティブLow) の場合はtrue、立ち上がりパルスの場合はfalseを選択します。

またPPSの入力を認識させるため
```
echo pps-gpio | sudo tee -a /etc/modules
```
と実行します。ここで一度再起動します。
```
sudo reboot
```

再起動後に必要なソフトウェアをインストールします。
```
sudo apt install -y gpsd gpsd-clients pps-tools
```

続いてgpsdの設定です。
```
sudo nano /etc/default/gpsd
```
として設定ファイルを開き、最後の行に
```
START_DAEMON="true"
DEVICES="/dev/ttyS0 /dev/pps0"
GPSD_OPTIONS="-n"
```
と追記し、
```
sudo systemctl enable gpsd.socket
```
として有効化します。GPS信号が受信できていれば
```
gpsmon
sudo ppstest /dev/pps0
```
といったコマンドでGPS信号の確認ができます。

NTPのソフトウェアとしてchronyをインストールします。
```
sudo apt -y install chrony
```

chronyの設定を変更するため
```
sudo nano /etc/chrony/chrony.conf
```
で設定ファイルを開きます。
```
sourcedir /run/chrony-dhcp
```
を#でコメントアウトし、
```
refclock PPS /dev/pps0 lock NMEA refid GPS
```
を追記します。
```
sudo systemctl restart chrony.service
```
でシステムを再起動します。

```
chronyc sources -v
```
でNTPの状況を確認できます。GPSによる時刻同期がされた場合はGPSのLEDが点灯します。


## 高度な設定

### 温度センサーのI2Cアドレス
温度センサーはI2Cで通信しています。動作確認は[秋月電子のAE-BME280](https://akizukidenshi.com/catalog/g/g109421/)で行っており、I2Cアドレスは0x76を選択しています。

他のBME280ベースのI2C通信対応の温度センサーを使用する場合で、異なるI2Cアドレスを使用する場合は、`~/git/pirad/scripts/python/control_hv.py`のaddress_tempを書き換えてください。なおHV制御用のDACもI2C通信で制御しており、そのアドレスは0x60を使用していますので、重複したアドレスを使用することはできません。

### HV制御のパラメータ
HVの電圧はHV生成用のICであるLT3482にリファレンス信号を入力して制御しています。リファレンス電圧はI2C通信対応の12-bit DACチップであるMCP4726で生成し、バッファーを通じてLT3482に入力されています。DACの制御パラメータ (最大12-bit = 4096) は出力電圧と一致するように以下の式に調整されています。
```
Channel = (HV+1.8821)/0.0213153
```
ただし出力電圧と設定ファイルでの指定電圧は抵抗など実装部品のKu世用特性によって変化することがあります。そのため、より精密な値を設定したい場合は、キャリブレーションしてパラメータを求めたうえで、`~/git/pirad/scripts/python/control_hv.py`のdac_constを変更してください。ただし予期せぬ値が代入された場合、高電圧が印加され、MPPCが故障する原因になりますので、接続する前にテスター等で出力電圧を確認してください。