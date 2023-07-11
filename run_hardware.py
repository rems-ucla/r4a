from BotRunnner import BotRunner

b = BotRunner(debug_mode=True)
# setup inputs
b.set_input(input_type='keyboard')
# Add robot to use
b.add_hardware(ip_address='ws://192.168.4.1:81')
# run the robto for 10 sec
b.run_robots(duration=10)
