from rems import Operator, SimConfig
from rems.inputs import FileCsvInput, KeyboardInput, JoystickInput
from rems.outputs import FileCsvOutput, AnimationOutput
from rems.utils import time_str
from robots import WoodbotHard, WoodbotModel
from mocap import ArucoBot, ENV
# Woodbot import
from robots import WoodbotDef

from warnings import warn

default_env = ENV()
default_env.WIDTH = 0.75
default_env.LENGTH = 0.45

class BotRunner:

    def __init__(self, debug_mode=False, output_path='./run_outputs/'):
        self.operator = Operator(debug_mode=debug_mode)
        self.output_path = output_path
        self.operator_inpt = None
        self.robots = []

    def set_input(self, input_type='keyboard', file_path='', *args, **kwargs):
        """

        :param input_type: 'keyboard', 'csv', or 'joystick'
        :return:
        """
        if input_type == 'csv':
            i = FileCsvInput(file_path)
        elif input_type == 'joystick':
            i = JoystickInput()
        elif input_type == 'keyboard':
            # Using  keyboard input (control Woodbot with arrow keys)
            # up: straight (100%, 100%), down: backward (-100, -100)
            # right: (100, 0), left: (0, 100)
            # up & right: (100, 50), up & left: (50, 100)
            # pageup: (-100, 100), pagedown: (100, -100)
            i = KeyboardInput()
        else:
            warn(f'input type {input_type} does not exist. Using Keyboard instead.')
            i = KeyboardInput()

        self.operator.set_input(i)

    def add_hardware(self, ip_address='ws://192.168.4.1:81', ):
        # Setup robot with output you want
        # robot def -> robot universal definitions such as state and input
        # robot -> is actual implemntation (your kinematics code)
        # outputs -> OutputSystem that show/record the data
        # FileCsvOutput -> save CSV file at the end of run with all inpt, state, output. (You can feed this file to FileCsvInput)
        # # AnimationOutput -> Show the robot states realtime and save the video of it at the end.
        robot = self.operator.add_robot(robot_def=WoodbotDef, robot=WoodbotHard,
                            robot_args=dict(target_address=ip_address),
                            outputs=self._setup_outputs('hard', animation=False))
        self.robots.append(robot)

    def add_analytical_model(self, motor_speed=None):
        # Setup robot with output you want
        # robot def -> robot universal definitions such as state and input
        # robot -> is actual implemntation (your kinematics code)
        # outputs -> OutputSystem that show/record the data
        # FileCsvOutput -> save CSV file at the end of run with all inpt, state, output. (You can feed this file to FileCsvInput)
        # # AnimationOutput -> Show the robot states realtime and save the video of it at the end.
        robot = self.operator.add_robot(robot_def=WoodbotDef, robot=WoodbotModel, def_args=dict(motor_speed=motor_speed),
                            outputs=self._setup_outputs('model'))
        self.robots.append(robot)

    def add_mocap(self, camera_id=0, track_tag=1, env=None):
        # Setup robot with output you want
        # robot def -> robot universal definitions such as state and input
        # robot -> is actual implemntation (your kinematics code)
        # outputs -> OutputSystem that show/record the data
        # FileCsvOutput -> save CSV file at the end of run with all inpt, state, output. (You can feed this file to FileCsvInput)
        # # AnimationOutput -> Show the robot states realtime and save the video of it at the end.
        if env is None:
            env = default_env
        robot = self.operator.add_robot(robot_def=None, robot=ArucoBot,
                            robot_args=dict(tracids=track_tag, camera_id=camera_id, filename=self._create_timestamp('mocap')+'.avi', env=env),  # probably camera id is 2, 1 or 0
                            outputs=self._setup_outputs('mocap'))
        self.robots.append(robot)

    def _setup_outputs(self, name, csv=True, animation=True):
        outpts = []
        file_name = self._create_timestamp(name)
        if csv:
            outpts.append(FileCsvOutput(file_name + '.csv'))
        if animation:
            outpts.append(AnimationOutput(file_name + '.gif', save_html_path=file_name + '.html'))

        return tuple(outpts)

    def _create_timestamp(self, name):
        return self.output_path + name + time_str() # this will be like: Model_current_data_tim

    def run_robots(self, duration, dt=0.05):
        """
        Run all the robots added to the system. At the end of execution, the output will be created.
        :param duration: ow long you want to run the robot.
        :return:
        """

        if self.operator_inpt is None:
            self.set_input()

        # run the robot for 10sec with dt = 0.1.
        # realtime=True, so it'll take 10sec to finish, False will run as fast as possible
        # start_time will let you start t=n. i.e. you want to run input file from t=5sec
        # run_speed multiply the realtime run speed. i.e. you want to debug the robot by running slow
        self.operator.run(SimConfig(max_duration=duration, dt=dt, realtime=True, start_time=0, run_speed=1))









