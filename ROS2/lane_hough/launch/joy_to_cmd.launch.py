from launch import LaunchDescription
from launch_ros.actions import Node



def generate_launch_description():
     
    joy = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        output='screen'
    )
    
    joy_to_cmd_vel = Node(
        package='joy_to_cmd',
        executable='joy_to_cmd_vel',
        name='joy_to_cmd_vel',
        output='screen'
    )
    
    
    serial_node = Node(
        package='lane_hough',
        executable='serial',
        name='serial',
        output='log',
        parameters=[{

        }])

    
    return LaunchDescription([
        joy,
        joy_to_cmd_vel,
        serial_node,

    ])