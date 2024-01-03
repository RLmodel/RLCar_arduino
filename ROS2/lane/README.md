# lane_arduino


## image_tools cam2image
$ ros2 run image_tools cam2image


## usb_cam
#$ ros2 run usb_cam usb_cam_node_exe --ros-args --params-file ~/ros2_ws/src/usb_cam/config/params_1.yaml


## Lane_detection && Publish twist_msg(cmd_vel)
$ ros2 run lane lane1


## sub msg && arduino Serial
$ ros2 run lane lane2


## or

$ ros2 run usb_cam usb_cam_node_exe --ros-args --params-file ~/ros2_ws/src/usb_cam/config/params_1.yaml

$ ros2 launch lane lane_detect.launch.py
