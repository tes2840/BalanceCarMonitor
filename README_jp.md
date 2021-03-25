[English](README.md) | Japanese  
# BalanceCarMonitor
BalaceCarMonitorは[BalanceCar](https://github.com/tes2840/BalanceCar)をネットワーク経由で操縦、チューニング、モニタリングすることができます。  

# DEMO
## 操縦デモ
[BalanceCar](https://github.com/tes2840/BalanceCar)を十字キーで操縦できます。  
十字キーの同時入力で、斜め方向への移動も可能です。  
![demo_operation](https://github.com/tes2840/BalanceCarMonitor/wiki/images/BalanceCarMonitor_Demo_Operation.gif)

## 設定デモ
[BalanceCar](https://github.com/tes2840/BalanceCar)の内部チューニングパラメータの設定が可能です。  
パラメータを変更したいときは、[BalanceCar](https://github.com/tes2840/BalanceCar)へソフトを書き込みする必要はなく、このツールで設定可能です。  
<img src="https://github.com/tes2840/BalanceCarMonitor/wiki/images/BalanceCarMonitor_Demo_Setting.png" width="540">

## 測定デモ
[BalanceCar](https://github.com/tes2840/BalanceCar)の内部状態が確認可能です。  
<img src="https://github.com/tes2840/BalanceCarMonitor/wiki/images/BalanceCarMonitor_Demo_Mesurement.gif" width="540">
 
# Requirement
## Libraries
BalanceCarMonitorの実行には、Python 3.8.5以降が必要です。  
macOSおよびWindowsでは、以下のサイトからダウンロードすることができます。  
https://www.python.org/getit/  

## Equipment
[BalanceCar](https://github.com/tes2840/BalanceCar)が必要です。さらなる情報はリンク先をご確認下さい。  

# Installation
pipコマンドでnumpy、 matplotlib、 kivyをインストールします。  
 
```bash
pip install numpy matplotlib kivy
```  

# Usage
このリポジトリをクローンし、フォルダの中に移動します。  
```bash
git clone https://github.com/tes2840/BalanceCarMonitor.git
cd BalanceCarMonitor
```
config.pyをご自身のネットワーク環境に合わせて設定してください。  

```python:config.py
config.BALAC_IP_ADDR= '192.168.11.101'  # BalanceCar's IP address.
config.BALAC_HOST   = ''                # BalanceCar's host name.
config.BALAC_PORT   = 50008             # BalanceCar's port.
config.PC_RECV_PORT = 50007             # Port of the PC running this application.
```
[BalanceCar](https://github.com/tes2840/BalanceCar)を起動します。  
gui.pyを実行します。  
```
python gui.py
```
 
# Note
macOS環境下ではテストしましたが、Linux、 Windows環境下ではテストしていません。  
 
# Author
github : [tes2840](https://github.com/tes2840/)  
Twitter : [@tes2840](https://twitter.com/tes2840)
 
# License
BalanceCarMonitorは[MIT license](https://en.wikipedia.org/wiki/MIT_License)に準拠します。  
