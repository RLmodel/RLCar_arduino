# hough transform (canny)


# for teensy

---

    ros2 run image_tools cam2image                  (for image_tools)

    ros2 run usb_cam usb_cam_node_exe               (for usb_cam)

    ros2 launch rplidar_ros rplidar_a2m8_launch.py        

    ros2 launch src_odometry src_bringup.launch.py         

    ros2 run lane_hough scan  

 
---


# for aruduino


 $ ros2 run image_tools cam2image                (for image_tools)

               or

 $ ros2 run usb_cam usb_cam_node_exe             (for usb_cam)

 $ ros2 launch rplidar_ros rplidar_a2m8_launch.py

 $ ros2 run lane_hough serial

 $ ros2 run lane_hough scan


---


## dependency

$ pip install opencv-python

$ pip install pyserial


## etc 

$ ls /dev/ttyUSB*    





+ for labtop users

$ ros2 run usb_cam usb_cam_node_exe --ros-args --params-file ~/ros2_ws/src/usb_cam/config/params_1.yaml

