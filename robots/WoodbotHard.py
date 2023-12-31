from rems.robots import RobotBase
from .WebsocketDevice import WebsocketDevice

from defdict.StdUnit import Pos, Vel, Ang, AngVel, AngAcc, UnitType, Percent
TARGET = "ws://192.168.4.1:81"


class Fs90r(AngVel):
    default_unit = 'rad/s'
    default_dtype = float
    default_drange = (-6.8, 6.8)

class Fs90rSend(Percent):
    default_unit = 'percent'
    default_dtype = float
    # data scale. (-1, 1) -> -100% to 100%. (0, 1) -> 0% to 100%
    defualt_drange_scale = (-1, 1)


class WoodbotHard(RobotBase):
    def __init__(self, target_address=TARGET, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.run.DT = 0.05
        self.target = target_address

    def init_devices(self):
        self.add_device(WebsocketDevice(target_address=self.target))

