import ControlBalac
import sin
import const

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import copy
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
        id: OperationTab
        text: 'Operation'
        GridLayout:
            id: OperationLayout
            rows: 3
            cols: 3
            Button:
            Button:
                id: UpButton
            Button:
            Button:
                id: LeftButton
            Button:
            Button:
                id: RightButton
            Button:
            Button:
                id: DownButton
            Button:
    
    TabbedPanelItem:
        id: SettingTab
        text: 'Setting'
        GridLayout:
            id: GridLayout
            rows: 8
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
            Label:
                text: 'Kspin'
            TextInput:
                id: Kspin
                text: ''
                multiline: False
                input_filter: 'float'
            Button:
                id: button
                text: "SET"
                font_size: 18
                on_press: root.on_command()
    
    TabbedPanelItem:
        id: MesurementTab
        text: 'Mesurement'
""")

# Balacのチューニングパラメータ
params = {
    'OPE_TYPE': 0,
    'Kang': 37.0,
    'Komg': 0.84,
    'KIang':800.0,
    'Kyaw': 4.0,
    'Kdst': 85.0,
    'Kspd': 2.7,
    'Kspin':10.0,
}

class GUI(TabbedPanel):
    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
        # set keybord config
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)

        # init input text
        for id in self.ids:
            if (id in params):
                self.ids[id].text = str(params[id])

        # グラフを描画するタブの設定
        # グラフを描画するTabbedPanelのインスタンスを取得
        self.panel = self.ids["MesurementTab"]

        # Balac
        self.balac = ControlBalac.ControlBalac("192.168.11.101", '', 50007,  50008, params )
        self.fig = self.balac.getFig()
        #Figure.canvas をウィジェットとしてPanelに追加する
        self.panel.add_widget(self.fig.canvas)

        # 操作初期設定
        self.operations = {
            'OPE_TYPE':1,
            'foward':0,
            'backward':0,
            'right':0,
            'left':0,
            'stand':1
        }
        self.operations_z1 =copy.copy(self.operations)

    def update(self, dt): # dt is delta time
        if (self.current_tab.text == 'Mesurement'):
            self.balac.recvData()
        #print("update_delta_time:",dt)

    def on_command(self, **kwargs):
        for id in self.ids:
            if (id in params):
                params[id] = self.ids[id].text
        
        # Balacにパラメータを設定
        print(params)
        self.balac.setParams(params)
    
    def _keyboard_closed(self):
        if (self.current_tab.text == 'Operation'):
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard.unbind(on_key_up=self._on_keyboard_up)
            self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if ( (keycode[1] == 'right') or (keycode[1] == 'left') or (keycode[1] == 'up') or (keycode[1] == 'down') ):
            self.operations['stand'] = 0
        else:    #十字キー以外は何もしない
            return True
        
        if keycode[1] == 'right':
            self.operations['right'] = 1
            self.ids['RightButton'].background_color = (2.58,2.79,3,1)
        elif keycode[1] == 'left':
            self.operations['left'] = 1
            self.ids['LeftButton'].background_color = (2.58,2.79,3,1)
        elif keycode[1] == 'up':
            self.operations['foward'] = 1
            self.ids['UpButton'].background_color = (2.58,2.79,3,1)
        elif keycode[1] == 'down':
            self.operations['backward'] = 1
            self.ids['DownButton'].background_color = (2.58,2.79,3,1)
        
        if (self.operations != self.operations_z1):
            self.operations_z1 =copy.copy(self.operations)
        else:
            # 前回と同じ操作内容の場合は何もしない
            return True

        print(self.operations)
        # Balacを操作
        self.balac.operateBalac(self.operations)
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        # reset background color of button
        if keycode[1] == 'right':
            self.operations['right'] = 0
            self.ids['RightButton'].background_color = (1,1,1,1)
        elif keycode[1] == 'left':
            self.operations['left'] = 0
            self.ids['LeftButton'].background_color = (1,1,1,1)
        elif keycode[1] == 'up':
            self.operations['foward'] = 0
            self.ids['UpButton'].background_color = (1,1,1,1)
        elif keycode[1] == 'down':
            self.operations['backward'] = 0
            self.ids['DownButton'].background_color = (1,1,1,1)
        else:    #十字キー以外は何もしない
            return True

        # 全てのキーが話されている場合は倒立状態にする
        if ( (self.operations['right'] == 0) and (self.operations['left'] == 0) and 
                (self.operations['foward'] == 0) and (self.operations['backward'] == 0) ):
            self.operations['stand'] = 1

        #前回値に反映
        self.operations_z1 =copy.copy(self.operations)

        print(self.operations)
        # Balacを操作
        self.balac.operateBalac(self.operations)
        return True

class ControlBalacGUI(App):
    def build(self):
        gui = GUI()
        Clock.schedule_interval(gui.update, 1.0/2.0)
        return gui

if __name__ == '__main__':
    ControlBalacGUI().run()