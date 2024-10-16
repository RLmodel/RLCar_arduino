#!/usr/bin/env bash

source /opt/ros/humble/setup.bash

source ~/ros2_ws/install/setup.bash

ros2 launch lane_hough lane_follow.launch.py
