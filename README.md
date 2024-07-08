## Test Command


[Terminal 1]

    ros2 run turtlesim turtlesim_node

[Terminal 2]

    ros2 run joy joy_node

[Terminal 3]

    ros2 run joystick_py joy_0709 --ros-args -r cmd_vel:=/turtle1/cmd_vel


[launch]
    
 ros2 launch joystick_py joy_to_cmd.launch.py

