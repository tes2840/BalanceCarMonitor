from socket import socket, AF_INET, SOCK_DGRAM
import json
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
class ControlBalac:
    def __init__(self, balac_ipAddr, host, recv_port,  send_port, params):
        # parameterの設定
        self.params = params

        # Network設定
        self.dstAddr = (balac_ipAddr, send_port)    # Balacへの送信先情報
        self.host = host
        self.recv_port = recv_port
        # ソケットを用意
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.s.bind((self.host, self.recv_port))

        # 初回受信
        msg, address = self.s.recvfrom(8192)
        data = json.loads(msg)
        time = data["time"]

        # Chartの作成
        plt.ion()                       # Turn the interactive mode on.
        self.fig = plt.figure(figsize=(8.0, 6.0))
        #Chartのインスタンスをlistに格納
        self.charts = []
        for info in chartInfos:
            self.charts.append( SignalChart(self.fig, info.fig_pos, info.title, info.t_label, info.y_label, info.y_min, info.y_max, time) )

    def getFig(self):
        return self.fig

    def recvData(self):
            msg, address = self.s.recvfrom(8192)
            data = json.loads(msg)

            # 取得したデータをグラフに反映
            time = data["time"]     #　経過時間
            keys = data.keys()      #　JsonObjectに含まれるキーの一覧
            for key in keys:
                for chart in self.charts:
                    if (chart.key == key):
                        signal = data[key]
                        chart.draw(time,signal)

            self.fig.tight_layout()      # グラフの文字がかぶらないようにする
            plt.pause(.01)               # グラフの更新

    def setParams(self, params):
        self.params = params

        # 送信
        data = json.dumps(self.params)
        data = data.encode('utf-8')

        # 受信側アドレスに送信
        self.s.sendto(data,self.dstAddr)

    def operateBalac(self, operations):
        # 送信
        data = json.dumps(operations)
        data = data.encode('utf-8')

        # 受信側アドレスに送信
        self.s.sendto(data,self.dstAddr)

    def closeBalac(self):
        # ソケットを閉じておく
        self.s.close()