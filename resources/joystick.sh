#!/usr/bin/env bash

source /opt/ros/humble/setup.bash

source ~/ros2_ws/install/setup.bash

ros2 launch joystick_py joy_to_cmd.launch.py
