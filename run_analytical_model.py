from BotRunnner import BotRunner

b = BotRunner(debug_mode=True)
# setup inputs
b.set_input(input_type='keyboard')
# Add robot to use
b.add_analytical_model()
# run the robto for 10 sec
b.run_robots(duration=10)








