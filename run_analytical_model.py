from BotRunnner import BotRunner

# TODO: Change duration if you want to run the robot longer
RUN_DURATION = 10
INPUT_TYPE = 'keyboard'

b = BotRunner(debug_mode=True)
# setup inputs
b.set_input(input_type=INPUT_TYPE)
# Add robot to use
b.add_analytical_model()
# run the robto for 10 sec
b.run_robots(duration=RUN_DURATION)








