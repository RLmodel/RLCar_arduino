from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    joy_node =  Node(
            package='joy',
            executable='joy_node',
            name='joy')
    
    joystick_node = Node(
            package='joystick_py',
            executable='joy_0709',
            # name='JoyToCmd1',
            emulate_tty=True,
        #     remappings=[('cmd_vel', 'turtle1/cmd_vel')]
    )


    return LaunchDescription([
        joy_node,
        joystick_node

  ])