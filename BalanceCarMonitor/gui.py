import control_balac
import config

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
    'Kang': config.INIT_KANG,
    'Komg': config.INIT_KOMG,
    'KIang':config.INIT_KIANG,
    'Kyaw': config.INIT_KYAW,
    'Kdst': config.INIT_KDST,
    'Kspd': config.INIT_KSPD,
    'Kspin': config.INIT_KSPIN,
}

pushed_button_color = (2.58,2.79,3,1)
released_button_color = (1,1,1,1)

class GUI(TabbedPanel):
    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
        # キーボードの設定
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)

        # SettingTabの設定
        # ラベルのテキストを設定
        for id in self.ids:
            if (id in params):
                self.ids[id].text = str(params[id])

        # MesurementTabの設定
        # MesurementTabのインスタンスを取得
        self.panel = self.ids["MesurementTab"]

        # ControlBalacのインスタンスを生成
        self.balac = control_balac.ControlBalac(config.BALAC_IP_ADDR, config.BALAC_HOST, config.PC_RECV_PORT,  config.BALAC_PORT, params )
        self.fig = self.balac.get_figure()          # matplotlibのfigureのインスタンスを取得
        self.panel.add_widget(self.fig.canvas)  # figure.canvasをウィジェットとしてPanelに追加する

        # Balacの操作コマンド初期設定
        self.operations = {
            'OPE_TYPE':1,       # 操作種別(0:設定変更, 1:移動操作)
            'foward':0,         # 前進(0:無効,1:有効)
            'backward':0,       # 後退(0:無効,1:有効)
            'right':0,          # 右旋回(0:無効,1:有効)
            'left':0,           # 左旋回(0:無効,1:有効)
            'stand':1           # 倒立(0:無効,1:有効)
        }
        self.operations_z1 =copy.copy(self.operations)  # Balac操作状態の前回値

    def update(self, dt): # dt is delta time
        if (self.current_tab.text == 'Mesurement'):
            self.balac.recv_data()
    
    def on_command(self, **kwargs):
        for id in self.ids:
            if (id in params):
                params[id] = self.ids[id].text
        
        # Balacにパラメータを設定
        if __debug__:
            print(params)
            
        self.balac.set_params(params)
    
    def _keyboard_closed(self):
        # OperationTab以外でキーボード操作した場合、別ウェジットでもキーボードを要求されたことになり本関数がcallbackされる
        if (self.current_tab.text == 'Operation'):  # OperationTabでcallbackされた場合はキーボードをunbindする
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard.unbind(on_key_up=self._on_keyboard_up)
            self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # 十字キー操作かの判定
        if ( (keycode[1] == 'right') or (keycode[1] == 'left') or (keycode[1] == 'up') or (keycode[1] == 'down') ):
            #十字キーで何かしら操作された場合は倒立状態を無効にする
            self.operations['stand'] = 0
        else:
            #十字キー以外は何もしない
            return True
        
        # 十字キーの操作に合わせOperationTabの画面更新、Balac操作コマンド作成
        if keycode[1] == 'right':
            self.operations['right'] = 1
            self.ids['RightButton'].background_color = pushed_button_color
        elif keycode[1] == 'left':
            self.operations['left'] = 1
            self.ids['LeftButton'].background_color = pushed_button_color
        elif keycode[1] == 'up':
            self.operations['foward'] = 1
            self.ids['UpButton'].background_color = pushed_button_color
        elif keycode[1] == 'down':
            self.operations['backward'] = 1
            self.ids['DownButton'].background_color = pushed_button_color
        
        # 前回と同じ操作コマンドを送信しないための判定
        if (self.operations == self.operations_z1):
            return True # 前回と同じ操作内容の場合は何もせず関数を抜ける
        
        if __debug__:
            print(self.operations)
        
        # Balacを操作
        self.balac.operate_balac(self.operations)
        self.operations_z1 =copy.copy(self.operations)  # 操作コマンドを前回値に保存
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        # 離された十字キーに合わせOperationTabの画面更新、Balac操作コマンド作成
        if keycode[1] == 'right':
            self.operations['right'] = 0
            self.ids['RightButton'].background_color = released_button_color
        elif keycode[1] == 'left':
            self.operations['left'] = 0
            self.ids['LeftButton'].background_color = released_button_color
        elif keycode[1] == 'up':
            self.operations['foward'] = 0
            self.ids['UpButton'].background_color = released_button_color
        elif keycode[1] == 'down':
            self.operations['backward'] = 0
            self.ids['DownButton'].background_color = released_button_color
        else:    #十字キー以外は何もしない
            return True

        # 全てのキーが離されている場合は倒立状態にする
        if ( (self.operations['right'] == 0) and (self.operations['left'] == 0) and 
                (self.operations['foward'] == 0) and (self.operations['backward'] == 0) ):
            self.operations['stand'] = 1
        
        if __debug__:
            print(self.operations)
        
        # Balacを操作
        self.balac.operate_balac(self.operations)
        self.operations_z1 =copy.copy(self.operations)  #　操作コマンドを前回値に反映
        return True

class ControlBalacGUI(App):
    def build(self):
        gui = GUI()
        Clock.schedule_interval(gui.update, 1.0/10.0)
        return gui

if __name__ == '__main__':
    ControlBalacGUI().run()