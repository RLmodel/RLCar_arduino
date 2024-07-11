# **hough transform (canny)**

---
### 실행방법


터미널에 아래 명령어를 통해 launch file을 실행할 수 있습니다.
&emsp;
    ros2 launch lane_hough lane_follow.launch.py

&emsp;

차량 별로 사용하는 카메라 패키지가 있습니다. ( image_tools && usb_cam )
 
 
다음과 같이 launch file에서 해당 차량에 맞는 노드를 활성화 시켜주면 됩니다.


< image_tools 패키지 활성화 >  # usb_cam 노드 비활성화



    
![Screenshot from 2024-07-11 10-01-22](https://github.com/RLmodel/RLCar_arudino/assets/151706131/9d53dc0d-43d0-42f0-b965-dd4bc84b1f90)



< usb_cam 패키지 활성화 >  # image_tools 노드 비활성화
![Screenshot from 2024-07-11 10-00-56](https://github.com/RLmodel/RLCar_arudino/assets/151706131/96a495ed-cd80-49ec-8397-424c15fa77a9)




***주의*** 차선인식 커맨드 실행 시 초기에 차선을 구분하지 못하면 해당 노드가 종료됩니다.
<br>
(초기 실행 시 카메라 각도 조정 필요)

***Tip*** 간단한 수정을 통해 더 나은 성능을 보일 수 있는 부분이 있습니다. 여러분들께서 찾아서 수정해주시면 됩니다.

*hint* : setup.py





--- 
## 개별 실행

### for aruduino (6번 차량 외)



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




---
### for teensy (6번 차량)


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

  


  
---


### dependency

    pip install opencv-python

    pip install pyserial

---

### etc 

    ls /dev/ttyUSB*    


위 커맨드로 아두이노 시리얼포트를 찾고 lane_serial.py 부분의 "/dev/ttyUSB1" 부분을 수정해주시면 됩니다.

---



+ for labtop users
#
    ros2 run usb_cam usb_cam_node_exe --ros-args --params-file ~/ros2_ws/src/usb_cam/config/params_1.yaml



