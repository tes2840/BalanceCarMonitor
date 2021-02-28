import ControlBalac
import sin
import const

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
# Kivy 上で Matplotlib を使うために必要な準備
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.clock import Clock
from kivy.core.window import Window
Window.size = (800, 640)

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
        GridLayout:
            id: GridLayout
            rows: 7
            cols: 2
            Label:
                text: 'Kang'
            TextInput:
                id: Kang
                text: ''
                multiline: False
                input_filter: 'float'
            Label:
                text: 'Komg'
            TextInput:
                id: Komg
                text: ''
                multiline: False
                input_filter: 'float'
            Label:
                text: 'KIang'
            TextInput:
                id: KIang
                text: ''
                multiline: False
                input_filter: 'float'
            Label:
                text: 'Kyaw'
            TextInput:
                id: Kyaw
                text: ''
                multiline: False
                input_filter: 'float'
            Label:
                text: 'Kdst'
            TextInput:
                id: Kdst
                text: ''
                multiline: False
                input_filter: 'float'
            Label:
                text: 'Kspd'
            TextInput:
                id: Kspd
                text: ''
                multiline: False
                input_filter: 'float'
            Button:
                id: button
                text: "SET"
                font_size: 18
                on_press: root.on_command()
""")

# Balacのチューニングパラメータ
params = {
    'Kang': 37.0,
    'Komg': 0.84,
    'KIang':800.0,
    'Kyaw': 4.0,
    'Kdst': 85.0,
    'Kspd': 2.7,
}

class GUI(TabbedPanel):
    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
        # set keybord config
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        # init input text
        for id in self.ids:
            if (id in params):
                self.ids[id].text = str(params[id])

        # グラフを描画するタブの設定
        # グラフを描画するTabbedPanelのインスタンスを取得
        self.panel = self.ids["MesurementTab"]

        # 描画するグラフを用意する
        #self.sin = sin.sin()
        #self.fig, self.ax = self.sin.getFig()

        # Balac
        self.balac = ControlBalac.ControlBalac("192.168.11.101", '', 50007,  50008, params )
        self.fig = self.balac.getFig()
        #Figure.canvas をウィジェットとしてPanelに追加する
        self.panel.add_widget(self.fig.canvas)

    def update(self, dt): # dt is delta time
        #self.sin.update(dt)
        self.balac.recvData()
        #print("update_delta_time:",dt)

    def on_command(self, **kwargs):
        for id in self.ids:
            if (id in params):
                params[id] = self.ids[id].text
        
        # Balacにパラメータを設定
        self.balac.setParams(params)
    
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        operations = {
            'foward':0,
            'backward':0,
            'right':0,
            'left':0
        }
        if keycode[1] == 'right':
            operations['right'] = 1
        elif keycode[1] == 'left':
            operations['left'] = 1
        elif keycode[1] == 'up':
            operations['foward'] = 1
        elif keycode[1] == 'down':
            operations['backward'] = 1
        print(operations)

        # Balacを操作
        self.balac.operateBalac(operations)
        return True


class ControlBalacGUI(App):
    def build(self):
        gui = GUI()
        Clock.schedule_interval(gui.update, 1.0/10.0)
        return gui

if __name__ == '__main__':
    ControlBalacGUI().run()