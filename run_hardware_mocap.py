from BotRunnner import BotRunner

b = BotRunner(debug_mode=False)
# setup inputs
b.set_input(input_type='keyboard')
# Add robot to use
b.add_hardware(ip_address='ws://192.168.4.1:81')
# TODO: Update your camera ID (usually 0, 1, 2)
b.add_mocap(camera_id=0, track_tag=1)
b.add_analytical_model() # analytical model
# run the robot for 10 sec
b.run_robots(duration=20)
