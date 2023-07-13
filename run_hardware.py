from BotRunnner import BotRunner

RUN_DURATION = 10
INPUT_TYPE = 'keyboard'

b = BotRunner(debug_mode=False)
# setup inputs
b.set_input(input_type=INPUT_TYPE)
# Add a robot to use. IP ip address is fixed.
b.add_hardware(ip_address='ws://192.168.4.1:81')
# run the robot for 10 sec
b.run_robots(duration=RUN_DURATION)
