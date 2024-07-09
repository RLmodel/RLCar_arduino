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

        global ser
        ser = serial.Serial("/dev/ttyUSB1", 115200)        # ls /dev/ttyUSB*
        self.op = 0


        self.get_logger().info('==== Lane_detection Started ====\n')
        

    def serial_callback(self, data):
        
        print(self.sub_cmd.msg_type)
        a = 100*data.linear.x       # linear.x = 0.5 == str(50)
        b = 2*data.angular.z       # linear.z = 0.5 == str(10)
        #print(a)
        #print(b)
           
        self.op = str(a)+"," + str(30+b)+",g,0,test_message &"
        op = self.op
        #print(op)
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
            