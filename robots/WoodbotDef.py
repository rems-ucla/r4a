from .DifferentialDriveBase import DifferentialDriveDef
from defdict.StdUnit import Pos, Vel, Ang, AngVel, AngAcc, UnitType, Percent



# Input definition
# We have two inputs: wh.l, wh.r
# their units are percentage in a range of -1, 1. meaning from -100% to 100%
# if both wheel velocity are at (1, 1) then robot is moving forward at the max speed
INPT = {
    'wh.l': Percent(scale=(-1, 1)), # keu name and data type
    'wh.r': Percent(scale=(-1, 1))
}

# State definition
# we have 4 state elements: x, y, th_z (rotation around z axis), d_th_z (angular velocity)
# their unit are as shown
# Pos , Ang, AngVel are our custom class that handle units for us
STATE = dict(x=Pos(unit='m'), y=Pos(unit='m'), th_z=Ang(unit='rad'), d_th_z=AngVel(unit='rad/s'))

# Output definitions
# we have 5 sensors:
# lidar_f, lidar_r, (lidar facing straight and side)
# mag_x, mag_y      (Magnetometer x and y component) in range of 0 to 1
#

OUTPUT = {
    'lidar_f': Pos(unit='m'),
    'lidar_r': Pos(unit='m'),
    'mag_x': Percent(scale=(0, 1)),
    'mag_y': Percent(scale=(0, 1)),
    'gyro_z': AngVel(unit='rad/s'),
}

DIMENSION = {'W': 0.1,
             'd': 0.04,
             'R_env': 0.4,
             'max_vel': 6.8}


class WoodbotDef(DifferentialDriveDef):
    def __init__(self, *args, **kwargs):
        DifferentialDriveDef.__init__(self, *args, **kwargs)
        # set definitions for self.inpt
        # self.inpt is a dictionary like custom object
        # we can treat like dictionary, but more functions
        self.inpt.add_def(INPT)
        self.state.add_def(STATE)
        self.outpt.add_def(OUTPUT)

        # adding dimension
        self.dimension.add_def(DIMENSION)

        # Robot name
        self.name = 'woodbot'





