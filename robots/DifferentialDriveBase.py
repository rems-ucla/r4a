from defdict import DefDict, MapRule
from rems.robots import RobotDefBase
from defdict.StdUnit import Pos, Vel, Ang, AngVel, AngAcc, Percent

from .WoodbotHard import WoodbotHard


# Woodbot Velocity unit
class WoodbotVel(AngVel):
    default_unit = 'rad/s'      # Physical Unit
    default_value = None        # Default, None uses dtype default (i.e. float() -> 0.0)
    default_dtype = float       # data type
    default_drange = (-8, 8)    # data range. You can specify the unit or it uses the default_unit
    default_drange_map = None   # Only for unitless quantity
    # data scale. (-1, 1) -> -100% to 100%. (0, 1) -> 0% to 100%. Used to convert the value in percentage
    defualt_drange_scale = (-1, 1)


WHEEEL_VEL = {'wh.l': Percent(scale=(-1, 1)), 'wh.r': Percent(scale=(-1, 1))}


def set_vel(o, t):
    t.vel().set_positional(o)
    t.pos().set([float('inf'), float('inf')])
    return t

rule_to_nested_vel = MapRule(['wh.l', 'wh.r'],
            set_vel,
            with_target=True)


webots_drive_rule = MapRule(['wh.l', 'wh.r'],
            set_vel,
            ['motor_r', 'motor_l'],
            with_target=True)


# Key mapping for keyboards and Joysticks
class KeyMapRule:
    def __init__(self):
        # MapRule class, this basically does:
        # target = rule_function(origin)
        self.arrow = MapRule(
            ['page_up', 'page_down', 'right', 'left', 'up', 'down'],            # origin keys
            self.arrow_drive,                                                   # rule_function
            {'wh.l': Percent(scale=(-1, 1)), 'wh.r': Percent(scale=(-1, 1))},   # target keys and data
            to_list=True)                                                       # this will make origin a list (ordered)
        self.direct = MapRule(['q', 'e', 'a', 'd'],
                              self.direct_drive,
                              WHEEEL_VEL,
                              to_list=True)
        self.joy_direct = MapRule(['STICK_LEFT_Y', 'STICK_RIGHT_Y'],
                                  self.joystick_drive,
                                  WHEEEL_VEL,
                                  to_list=True)

    def get_rules(self):
        return [self.arrow]

    def direct_drive(self, l, r, l_b=None, r_b=None):
        if l_b: l*=-1
        elif r_b: r*=-1
        return 100*l, 100*r

    def joystick_drive(self, l_y, r_y):
        return 100*l_y, 100*r_y



    def arrow_drive(self, page_up, page_down, right, left, up, down):
        ret = (0, 0)
        if page_up: ret = (-1, 1)
        elif page_down: ret = (1, -1)
        elif up and right: ret = (1, 0.5)
        elif up and left: ret = (0.5, 1)
        elif down and right: ret = (-1, -0.5)
        elif down and left: ret = (-0.5, -1)
        elif right: ret = (1, 0)
        elif left: ret = (0, 1)
        elif up: ret = (1, 1)
        elif down: ret = (-1, -1)
        return self.direct_drive(*ret)


class DifferentialDriveDef(RobotDefBase):
    def __init__(self, *args, **kwargs):
        RobotDefBase.__init__(self, *args, **kwargs)
        self.dimension = DefDict()

    def define(self, *args, **kwargs):
        """Definitions of the robot"""

        # Adding mapping rule to the input
        # i.e. from keyboard arrow to left right wheel speed
        self.inpt.set_rule([KeyMapRule().arrow, KeyMapRule().joy_direct])

        # Sensor space definitions
        SENSOR = {"Webots": self.outpt.dict(),
                  "Woodbot": WoodbotHard.sense_space_def()
                  }

        wb_drive = DefDict({
            "motor_l": dict(pos=Ang(default=float('inf')), vel=WoodbotVel, acc=AngAcc, on=bool, pid=list),
            "motor_r": dict(pos=Ang(default=float('inf')), vel=WoodbotVel, acc=AngAcc, on=bool, pid=list),
        }, rules=webots_drive_rule)


        # motor space definitions
        DRIVE = {
            "Webots": wb_drive,
            "Woodbot": WoodbotHard.drive_space_def(),
            # "model":
        }

        self.drive_space.add_def(DRIVE)
        self.sense_space.add_def(SENSOR)
        super().define()
