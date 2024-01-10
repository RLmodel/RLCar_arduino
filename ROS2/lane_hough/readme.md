# hough transform (canny)


# for teensy



## $ ros2 run image_tools cam2image                (for image_tools)

## $ ros2 run usb_cam usb_cam_node_exe             (for usb_cam)

## $ ros2 launch src_odometry src_bringup.launch.py    

## $ ros2 run lane_hough hough



# for aruduino


## $ ros2 run image_tools cam2image                (for image_tools)

## $ ros2 run usb_cam usb_cam_node_exe             (for usb_cam)

## $ ros2 run lane_hough hough                      

## $ ros2 run lane_hough serial


$ pip install opencv-python

$ pip install pyserial

check the serail port 

$ ls /dev/ttyUSB*    

![download](https://github.com/RLmodel/RLCar_examples/assets/151706131/d62f1b0b-8a7d-4bd5-96bc-ce40ff445685)


























+ for labtop users

$ ros2 run usb_cam usb_cam_node_exe --ros-args --params-file ~/ros2_ws/src/usb_cam/config/params_1.yaml

