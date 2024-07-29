import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription

def generate_launch_description():
                

    ## image_tools 사용시 활성화

    cam_node = ExecuteProcess(
        cmd=[[
            "ros2 run image_tools cam2image ",
            "--ros-args --log-level ",
            "error"
        ]], 
        shell=True
    )
    
    ## usb_cam 사용시 활성화

    # cam_node = Node(                
    #     package='usb_cam',
    #     executable='usb_cam_node_exe',
    #     name='usb_cam',
    #     output='log',
    #     parameters=[{
    #         'video_device' : '/dev/video0'   # 외부 카메라 사용 시, 또는 /dev/video 인식 오류 시 수정
    #     }]
    # )
    

    rplidar_ros2_pkg = os.path.join(get_package_share_directory('rplidar_ros'))
    rplidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(rplidar_ros2_pkg, 'launch', "rplidar_a2m8_launch.py"))
    )
    
    
    serial_node = Node(
        package='lane_hough',
        executable='serial',
        name='serial',
        output='log',
    )
    
    lane_node = Node(
        package='lane_hough',
        executable='scan',
        name='scan',
        output='log',
        parameters=[{
            'is_image_tools' : True,   # image_tools 사용시 True, usb_cam 사용시 False 

            'velocity': 0.6,            
                                        # Min(0.0) ~ Max(2.0) , 
                                        # 차량마다 모터가 구동될 수 있도록 하는 최소 파라미터가 다르므로
                                        # 모터가 작동하지 않을 시에 값을 키우면서 파라미터를 찾으시면 됩니다.

            'steering' : 0.7,           
                                        # 조향에 대한 파라미터입니다. 값이 작을수록 적게 조향되고 클수록 많이 조향됩니다. 
                                        # (0.2 ~ 1.5) 사이에서 조정하시는 것을 권장드립니다.
        }])

    return LaunchDescription([
        cam_node,
        rplidar_launch,
        serial_node,
        lane_node,
    ])