import os
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    lane1 = Node(
        package='lane',
        executable='lane1',
        name='lane1',
        output='screen'
    )

    lane2 = Node(
        package='lane',
        executable='lane2',
        name='lane2',
        output='screen'
    )


    return LaunchDescription([
        lane1,
        lane2,
        
    ])
