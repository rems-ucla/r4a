from rems import Operator, SimConfig
from rems.inputs import FileCsvInput, KeyboardInput, JoystickInput
from rems.outputs import FileCsvOutput, AnimationOutput
from rems.utils import time_str
from robots import WoodbotHard
from mocap import ArucoBot
# Woodbot import
from robots import WoodbotDef

USE_TRAJECTORY = 'traj'
USE_JOYSTICK = 'joystick'
USE_KEYBOARD = 'keyboard'

OUTPUT_PATH = '../run_outputs/'
FILE_PATH = OUTPUT_PATH + 'Woodbot' + time_str() # this will be like: Model_current_data_tim
CAMERA_FILE_PATH = OUTPUT_PATH + 'aruco' + time_str() # this will be like: Model_current_data_time# e

# if you want to use pre defined trajectory
MODE = USE_TRAJECTORY
MODE = USE_JOYSTICK
MODE = USE_KEYBOARD


# a nice function to automatically update the dependency
# rems_update()

# REMS robot operator
# this take care lower level operations
o = Operator(debug_mode=True)


if MODE == USE_TRAJECTORY:
    i = FileCsvInput('traj/example_traj.csv')
elif MODE == USE_JOYSTICK:
    i = JoystickInput()
else:
    # Using  keyboard input (control Woodbot with arrow keys)
    # up: straight (100%, 100%), down: backward (-100, -100)
    # right: (100, 0), left: (0, 100)
    # up & right: (100, 50), up & left: (50, 100)
    # pageup: (-100, 100), pagedown: (100, -100)
    i = KeyboardInput()

#  set input
o.set_input(i)

# Setup robot with output you want
# robot def -> robot universal definitions such as state and input
# robot -> is actual implemntation (your kinematics code)
# outputs -> OutputSystem that show/record the data
# FileCsvOutput -> save CSV file at the end of run with all inpt, state, output. (You can feed this file to FileCsvInput)
# # AnimationOutput -> Show the robot states realtime and save the video of it at the end.
#
robot = o.add_robot(robot_def=WoodbotDef, robot=WoodbotHard,
                    robot_args=dict(target_address='ws://192.168.8.200'),
                    outputs=(FileCsvOutput(FILE_PATH + '.csv'),))

aruco = o.add_robot(robot_def=None, robot=ArucoBot,
                    robot_args=dict(tracids=1, camera_id=1,), # probably camera id is 2 or 1
                    outputs=(FileCsvOutput(CAMERA_FILE_PATH + '.csv'),
                             AnimationOutput(CAMERA_FILE_PATH + '.gif')))


# run the robot for 10sec with dt = 0.1.
# realtime=True, so it'll take 10sec to finish, False will run as fast as possible
# start_time will let you start t=n. i.e. you want to run input file from t=5sec
# run_speed multiply the realtime run speed. i.e. you want to debug the robot by running slow
o.run(SimConfig(max_duration=30, dt=0.1, realtime=True, start_time=0, run_speed=1))

