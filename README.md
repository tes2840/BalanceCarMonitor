English | [Japanese](README_jp.md)  
# BalanceCarMonitor
If you use BalanceCarMonitor, you can maneuver, tune parameters and monitor [BalanceCar](https://github.com/tes2840/BalanceCar) over the network.  

# DEMO
## Maneuver demo 
You can maneuver [BalanceCar](https://github.com/tes2840/BalanceCar) with the cross key and also move it diagonally by inputting the cross key at the same time.  
![demo_operation](https://github.com/tes2840/BalanceCarMonitor/wiki/images/BalanceCarMonitor_Demo_Operation.gif)

## Setting demo
You can set the tuning parameters of [BalanceCar](https://github.com/tes2840/BalanceCar).  
If you want to change the parameters, you do not need to write the software to [BalanceCar](https://github.com/tes2840/BalanceCar), you can set it with this tool.  
<img src="https://github.com/tes2840/BalanceCarMonitor/wiki/images/BalanceCarMonitor_Demo_Setting.png" width="540">

## Measurement demo  
You can check the status of [BalanceCar](https://github.com/tes2840/BalanceCar).   
<img src="https://github.com/tes2840/BalanceCarMonitor/wiki/images/BalanceCarMonitor_Demo_Mesurement.gif" width="540">
 
# Requirement
## Libraries
You need Python 3.8.5 or later to run BalanceCarMonitor.  
macOS and Windows, packages are available at  
https://www.python.org/getit/

## Equipment
You need [BalanceCar](https://github.com/tes2840/BalanceCar). Please check the link for further information.    

# Installation
Install numpy, matplotlib, and kivy with pip command.
 
```bash
pip install numpy matplotlib kivy
```  

# Usage 
Clone this repository and go into it. 
```bash
git clone https://github.com/tes2840/BalanceCarMonitor.git
cd BalanceCarMonitor
```
Please configure config.py to match your network environment.  

```python:config.py
config.BALAC_IP_ADDR= '192.168.11.101'  # BalanceCar's IP address.
config.BALAC_HOST   = ''                # BalanceCar's host name.
config.BALAC_PORT   = 50008             # BalanceCar's port.
config.PC_RECV_PORT = 50007             # Port of the PC running this application.
```
Start [BalanceCar](https://github.com/tes2840/BalanceCar).  
Run gui.py.
```
python gui.py
```
 
# Note
I have tested it under macOS, but not under Linux or Windows.   
 
# Author
github : [tes2840](https://github.com/tes2840/)  
Twitter : [@tes2840](https://twitter.com/tes2840)
 
# License
BalanceCarMonitor is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
