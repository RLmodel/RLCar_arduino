#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Serial(Node):

    def __init__(self):
        super().__init__('Serial')
        
        self.sub_cmd = self.create_subscription(String,'/cmd_h', self.serial_callback, 10) 

        global ser
        ser = serial.Serial("/dev/ttyUSB0", 115200)
        self.op = 0


        # self.get_logger().info('==== Lane_detection Started ====\n')
        

    def serial_callback(self, msg):
        
        
        op = self.op
        data = msg.data
        print(msg.data)

        if "up" in data:
            op = "up"

        elif "down" in data:
            op = "down"

        elif "stop" in data:
            op = "stop"

        elif "emerg" in data:
            op = "emerg"

        ser.write(op.encode())

def main(args=None):
    rclpy.init(args=args)
    serial_pub = Serial()

    try:
        rclpy.spin(serial_pub)

    except KeyboardInterrupt:
        serial_pub.get_logger().info('stopped')
    
    finally:
        serial_pub.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
            