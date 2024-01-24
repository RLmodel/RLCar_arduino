# **hough transform (canny)**

---

### for aruduino (6번 차량 외)
    
    
카메라는 아래 두 커맨드 중 각 차량에 맞게 한 개만 실행합니다. 

(총 4개 터미널 사용)

차선인식 커맨드 실행 시 초기에 차선을 구분하지 못하면 해당 노드가 종료됩니다.

(초기 실행 시 카메라 조정 필요)

##### **camera(for image_tools)**
        ros2 run image_tools cam2image          
##### **camera(for usb_cam)**
        ros2 run usb_cam usb_cam_node_exe          
##### **rplidar_ros**
        ros2 launch rplidar_ros rplidar_a2m8_launch.py  
##### **serial**
        ros2 run lane_hough serial  
##### **lane_detection && steering && stop**
        ros2 run lane_hough scan  

  

  *hint : setup.py
---
### for teensy (6번 차량)

---
##### **camera(for image_tools)**
        ros2 run image_tools cam2image                          
##### **camera(for usb_cam)**
        ros2 run usb_cam usb_cam_node_exe                      
##### **rplidar_ros**
        ros2 launch rplidar_ros rplidar_a2m8_launch.py                
##### **scr_odometry**
        ros2 launch src_odometry src_bringup.launch.py                 
##### **lane_detection && steering && stop**
        ros2 run lane_hough scan          

  

  *hint : setup.py
---





### dependency

$ pip install opencv-python

    $ pip install pyserial    


### etc 

$ ls /dev/ttyUSB*    





+ for labtop users

$ ros2 run usb_cam usb_cam_node_exe --ros-args --params-file ~/ros2_ws/src/usb_cam/config/params_1.yaml

