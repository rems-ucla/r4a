from BotRunnner import BotRunner


# TODO: Update your camera ID (usually 0, 1, 2)
CAMERA_ID = 0

# TODO: Change run duration if you want to run the robot longer or shorter.
RUN_DURATION = 20

INPUT_TYPE = 'keyboard'

# Initialization
b = BotRunner(debug_mode=False)

# setup inputs
b.set_input(input_type=INPUT_TYPE)

# Add robot to use
b.add_hardware(ip_address='ws://192.168.4.1:81')

b.add_mocap(camera_id=CAMERA_ID, track_tag=1)

b.add_analytical_model() # analytical model

# run the robot for 20 sec
b.run_robots(duration=RUN_DURATION)
