from socket import socket, AF_INET, SOCK_DGRAM
import json
#plot
import numpy as np
from matplotlib import pyplot as plt
from dataclasses import dataclass

#################### 定義 #########################
# リアルタイムプロット
class SignalChart:
    def __init__(self, fig, fig_pos, title, t_label, y_label, y_min, y_max, init_t ):
        self.t = np.zeros(100)
        self.y = np.zeros(100)
        self.init_t = float(init_t)
        self.key = title
        #self.resolution = (abs(y_min)+abs(y_max))/1023

        self.ax = fig.add_subplot(fig_pos)
        self.line, = self.ax.plot(self.t, self.y)
        self.ax.set_ylim(y_min, y_max)      #軸のyの下限、上限を設定
        #ラベルの設定
        self.ax.set_xlabel(t_label)
        self.ax.set_ylabel(y_label)
        self.ax.set_title(title)

    def draw(self, time, data):
        # 配列をキューと見たてて要素を追加・削除
        self.t = np.append(self.t, (float(time)-self.init_t))
        self.t = np.delete(self.t, 0)
        self.y = np.append(self.y, float(data))
        self.y = np.delete(self.y, 0)

        self.line.set_data(self.t, self.y)        
        self.ax.set_xlim(min(self.t), max(self.t))
    # キーを取得する
    def getKey(self):
        return self.key

@dataclass
class ChartInfo:
    fig_pos:    int     #Chartを表示する位置
    title:      str     #Chartのタイトル
    t_label:    str     #x軸のラベル
    y_label:    str     #y軸のラベル
    y_min:      int     #y軸の最小値
    y_max:      int     #y軸の最大値

# Chartの情報管理テーブル（Chartを追加したい場合はここに追記する)
chartInfos = [
    #         position,  title,      t_label,    y_label,                    y_min, y_max
    ChartInfo(331,       "gyro_X",   "time[s]",  "Angular velocity[rad/s]",  -50,    50),
    ChartInfo(332,       "gyro_Y",   "time[s]",  "Angular velocity[rad/s]",  -100,   100),
    ChartInfo(333,       "gyro_Z",   "time[s]",  "Angular velocity[rad/s]",  -100,   100),
    ChartInfo(334,       "acc_X",   "time[s]",  "velocity[m/s]",             -2,   2),
    ChartInfo(335,       "acc_Z",   "time[s]",  "velocity[m/s]",             -1,   1),
    ChartInfo(336,       "aveAccZ",   "time[s]",  "velocity[m/s]",           -1,   1),
    ChartInfo(337,       "aveAbsOmg",   "time[s]",  "ngular velocity[rad/s]", 0,   2)
]

#################### ロジック #########################
HOST = ''   
PORT = 50007

# 受信側アドレスをtupleに格納
dstAddr = ("192.168.11.101",50008)

# ソケットを用意
s = socket(AF_INET, SOCK_DGRAM)
# バインドしておく
s.bind((HOST, PORT))

# 初回受信
msg, address = s.recvfrom(8192)
data = json.loads(msg)
time = data["time"]

#Chartの作成
fig = plt.figure(1)
#Chartのインスタンスをlistに格納
charts = []
for info in chartInfos:
    charts.append( SignalChart(fig, info.fig_pos, info.title, info.t_label, info.y_label, info.y_min, info.y_max, time) )

# Main loop
while True:
    # 受信
    msg, address = s.recvfrom(8192)
    data = json.loads(msg)

    print(data)
    #print(f"message: {msg}\nfrom: {address}")

    # 取得したデータをグラフに反映
    time = data["time"]     #　経過時間
    keys = data.keys()      #　JsonObjectに含まれるキーの一覧
    for key in keys:
        for chart in charts:
            if (chart.key == key):
                signal = data[key]
                chart.draw(time,signal)
    
    fig.tight_layout()      # グラフの文字がかぶらないようにする
    plt.pause(.01)

    # 送信
    data = "{\"Kang\":37.0, \"Komg\":0.84, \"KIang\":800.0, \"Kyaw\":4.0, \"Kdst\":85.0, \"Kspd\":2.7}"
    data = data.encode('utf-8')

    # 受信側アドレスに送信
    s.sendto(data,dstAddr)

# ソケットを閉じておく
s.close()