from mocap import run_test

# TODO: Update your camera ID (usually 0, 1, 2)
CAMERA_ID = 0

# TODO: Change run duration if you want to run the robot longer or shorter.
RUN_DURATION = 20


run_test(camera_id=CAMERA_ID, track_tag=1, duration=RUN_DURATION)
