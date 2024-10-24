from launch import LaunchDescription

from launch.actions import DeclareLaunchArgument

from launch.substitutions import EnvironmentVariable, LaunchConfiguration

from launch_ros.actions import Node


a = DeclareLaunchArgument('node_prefix',
                          #default_value=[EnvironmentVariable('USER'), '_'],
                          default_value="True",
                          description='prefix for node name')
    
print(a.default_value)