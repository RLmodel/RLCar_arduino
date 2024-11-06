### RLCar Setup && TroubleShooting

https://water-proof-well.notion.site/RLCar-HUMBLE-129c26cd63ac8004a02bd89061a41dcb?pvs=4

<br/>

-----

## lane_dection && manaul state machine mode

<br/>

![joystick_manual](https://github.com/user-attachments/assets/0d52da52-795c-49db-9631-2bd5cd4621d7)

<br/>

move to ~/workspace/Source Folder

```bash
cd ~/ros2_ws/src
```

<br/>

clone RLCar_arduino

```bash
git clone https://github.com/RLmodel/RLCar_arduino.git
```

<br/>

clone rplidar c1 pkg

```bash
git clone -b ros2 https://github.com/Slamtec/rplidar_ros.git
```

<br/>

move to workspace && sourcing

```bash
cd ~/ros2_ws/
humble
```

<br/>

build && sourcing

```bash
cbp lane_hough
cbp joystick_py
cbp rplidar_ros
humble
```

<br/>

start driving

```bash
ros2 launch lane_hough lane_state.launch.py
```


<br/>

---
## joystick control only (manual mode)

<br/>

[Teminal 1]

<br/>

```bash
ros2 launch joystick_py joy_to_cmd.launch.py
```

<br/>

[Teminal 2]

<br/>

```bash
ros2 run lane_hough serial
```


<br/>

-----

# RLCar_arduino
RLCar arduino nano controller version example code sources

![RLCar protocol](https://github.com/RLmodel/RLCar_examples/assets/32663016/cd48e448-543a-4fa1-9cb9-6dc534248f62)

![RLCar python vscode](https://github.com/RLmodel/RLCar_examples/assets/32663016/c4755f75-ee9e-49e3-a644-b3255497b7d9)

![20230507_102923](https://github.com/RLmodel/RLCar_examples/assets/32663016/6c58d00c-3b32-47a8-96cd-43b2b0dcf592)

![Screenshot from 2023-12-19 18-25-38 (1)](https://github.com/RLmodel/RLCar_examples/assets/32663016/9b055f1f-4d0f-4ff6-a4be-e9a91b61590b)

![Screenshot from 2023-12-19 18-25-02 (1)](https://github.com/RLmodel/RLCar_examples/assets/32663016/1596c454-72bd-4acf-ba3f-b578542d5fde)
>>>>>>> 8d8fb9fda4a8468231fddc3f5e3042d8ac377735
