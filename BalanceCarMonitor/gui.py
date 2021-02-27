import ControlBalac
import sin

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
# Kivy 上で Matplotlib を使うために必要な準備
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.clock import Clock
from kivy.lang import Builder
Builder.load_string("""
<GUI>:
    do_default_tab: False

    TabbedPanelItem:
        id: MesurementTab
        text: 'Mesurement'

    TabbedPanelItem:
        id: SettingTab
        text: 'Setting'
        BoxLayout:
            Label:
                text: 'Second tab content area'
            Button:
                text: 'Button that does nothing'
""")

class GUI(TabbedPanel):
    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)

        # グラフを描画するタブの設定
        # グラフを描画するTabbedPanelのインスタンスを取得
        self.panel = self.ids["MesurementTab"]

        # 描画するグラフを用意する
        #self.sin = sin.sin()
        #self.fig, self.ax = self.sin.getFig()

        # Balac
        self.balac = ControlBalac.ControlBalac("192.168.11.101", '', 50007,  50008 )
        self.fig = self.balac.getFig()
        #Figure.canvas をウィジェットとしてPanelに追加する
        self.panel.add_widget(self.fig.canvas)

    def update(self, dt): # dt is delta time
        #self.sin.update(dt)
        self.balac.recvData()
        #print("update_delta_time:",dt)


class ControlBalacGUI(App):
    def build(self):
        gui = GUI()
        Clock.schedule_interval(gui.update, 1.0/60.0)
        return gui

if __name__ == '__main__':
    ControlBalacGUI().run()