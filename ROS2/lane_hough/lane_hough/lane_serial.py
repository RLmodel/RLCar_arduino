#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from geometry_msgs.msg import Twist
import serial
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64

class Serial(Node):

    def __init__(self):
        super().__init__('Serial')

        self.sub_cmd = self.create_subscription(Twist,'/cmd_vel', self.serial_callback, 10)
        # self.pub_encoder = self.create_publisher(Int64, 'encoder_pos_', 10)
        self.ser = serial.Serial("/dev/ttyNANO", 115200)        # ls /dev/ttyUSB*
        self.op = 0

        self.get_logger().info('==== Lane_detection Started ====\n')
        self.ser.reset_input_buffer()

    def serial_callback(self, data):
        
        ser = self.ser
        #print(self.sub_cmd.msg_type)
        a = 100*data.linear.x       
        b = 20*data.angular.z       
        # if b < 0:
        #     b += 13
        
        if a >= 0:
            self.op = str(abs(a))+"," + str(b+30)+",g,0,test_message &"
        
        elif a < 0:
            self.op = str(abs(a))+"," + str(b+30)+",b,1,test_message &"
            
        ser.write(self.op.encode())
        
        # ser.timeout = 0.1
        # if ser.in_waiting > 0:
        #     line = ser.readline().decode().strip()
        #     if line:
        #         print(line)
        #         line = int(line)
        #         ser.reset_input_buffer()
        #         # print(type(line))
        #         msg = Int64()
        #         msg.data = line
        #         self.pub_encoder.publish(msg)
        
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
            