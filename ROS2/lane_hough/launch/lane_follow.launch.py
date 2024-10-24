import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription


def generate_launch_description():
    
    # cam_node = Node(              # image_tools 사용시 활성화
    #     package='image_tools',
    #     executable='cam2image',
    #     name='cam2image',
    #     output='log'
    # )
    config = os.path.join(
        get_package_share_directory('lane_hough'),
        'config',
        'lane.yaml'
        )
        

    cam_node = Node(                # usb_cam 사용시 활성화
        package='usb_cam',
        executable='usb_cam_node_exe',
        name='usb_cam',
        output='log',
        parameters=[{
            'video_device' : '/dev/video0'   # 외부 카메라 사용 시, 또는 /dev/video 인식 오류 시 수정
        }]
    )
    
    rplidar_ros2_pkg = os.path.join(get_package_share_directory('rplidar_ros'))
    rplidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(rplidar_ros2_pkg, 'launch', "rplidar_a2m8_launch.py"))
    )
    
    
    serial_node = Node(
        package='lane_hough',
        executable='serial',
        name='serial',
        output='log',
        parameters=[{

        }])
    
    lane_node = Node(
        package='lane_hough',
        executable='scan',
        name='scan',
        output='log',
        parameters=[config])
    
    return LaunchDescription([
        cam_node,
        rplidar_launch,
        serial_node,
        lane_node,
    ])