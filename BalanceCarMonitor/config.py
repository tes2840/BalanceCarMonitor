"""
Constant types in Python.
"""
from dataclasses import dataclass

class config:
    class ConstError(TypeError):
        pass
 
    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value
 
import sys
sys.modules[__name__]=config()


# Define
# Balacのネットワーク設定
config.BALAC_IP_ADDR= '192.168.11.101'  # BalanceCar's IP address.
config.BALAC_HOST   = ''                # BalanceCar's host name.
config.BALAC_PORT   = 50008             # BalanceCar's port.
config.PC_RECV_PORT = 50007             # Port of the PC running this application.

# Balacのチューニングパラメータ初期値
config.INIT_KANG    = 37.0
config.INIT_KOMG    = 0.84
config.INIT_KIANG   = 800.0
config.INIT_KYAW    = 4.0
config.INIT_KDST    = 85.0
config.INIT_KSPD    = 2.7
config.INIT_KSPIN   = 10.0