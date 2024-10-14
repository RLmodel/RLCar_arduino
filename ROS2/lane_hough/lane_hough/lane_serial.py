#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from geometry_msgs.msg import Twist
import serial
import rclpy
from rclpy.node import Node


class Serial(Node):

    def __init__(self):
        super().__init__('Serial')

        self.sub_cmd = self.create_subscription(Twist,'/cmd_vel', self.serial_callback, 10) 
        self.ser = serial.Serial("/dev/ttyNANO", 115200)        # ls /dev/ttyUSB*
        self.op = 0
        
        self.get_logger().info('==== Lane_detection Started ====\n')
        

    def serial_callback(self, data):
        
        ser = self.ser
        #print(self.sub_cmd.msg_type)
        a = 200*data.linear.x       
        b = 20*data.angular.z       
        # if b < 0:
        #     b += 13
        
        if a >= 0:
            self.op = str(abs(a))+"," + str(38+b)+",g,0,test_message &"
        
        elif a < 0:
            self.op = str(abs(a))+"," + str(38+b)+",b,0,test_message &"
            
        
        ser.write(self.op.encode())

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
            