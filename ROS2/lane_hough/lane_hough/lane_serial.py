#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from geometry_msgs.msg import Twist
import serial
import rclpy
from rclpy.node import Node
import time

import rclpy.time



def connect_serial(port, baudrate:int = 115200)-> serial.Serial:
    count = 1
    while True:
        try: 
            ser = serial.Serial(port, baudrate)
            print("Serial connection Succeed")
            return ser
        except serial.SerialException:
            if count > 9:
                print("timeout")
                exit()
            print("Serial is not connected, waiting reconnection ... ({})".format(count))
            time.sleep(1)
            count += 1


def is_connected(ser: serial.Serial):
    try:
        response = ser.read()
        return len(response) > 0
    
    except serial.SerialException:
        return False

class Serial(Node):

    def __init__(self):
        super().__init__('Serial')

        self.sub_cmd = self.create_subscription(Twist,'/cmd_vel', self.serial_callback, 10) 
        self.declare_parameter("port", "/dev/ttyNANO")
        self.port_name_ = self.get_parameter("port").get_parameter_value().string_value
        
        
        self.ser = connect_serial(self.port_name_)

        time.sleep(2)

        self.op = 0
        self.allign = 27

        self.get_logger().info("Serial connected, port name : {}".format(self.port_name_))
        

    def __del__(self):
        self.op = str(0)+"," + str(26)+",g,0,test_message &"
        self.ser.write(self.op.encode()) 
    
    def serial_callback(self, data):
        
        #print(self.sub_cmd.msg_type)
        a = 200*data.linear.x       
        b = 20*data.angular.z       
        # if b < 0:
        #     b += 13
        if b > self.allign:
            b = self.allign
        if a >= 0:
            self.op = str(abs(a))+"," + str(self.allign-b)+",g,0,test_message &"
        
        elif a < 0:
            self.op = str(abs(a))+"," + str(self.allign-b)+",b,0,test_message &"
        
        # self.ser.write(self.op.encode())
        if is_connected(self.ser):
            try:
                self.ser.write(self.op.encode())
                
            except serial.SerialException:
                self.get_logger().info("Serial disconnected, recovery mode start")
                self.ser = serial.Serial(self.port_name_, 115200)
                
            # else:
            #     print("test command1")

            # finally:
            #     pass

        else: 
            while True:
                try:
                    self.ser = serial.Serial(self.port_name_, 115200)
                except serial.SerialException:
                    self.get_logger().info("Serial disconnected, retry connection")
                    time.sleep(1)
                else:
                    self.get_logger().info("Serial Connected")
                    break

                
                

def main(args=None):
    rclpy.init(args=args)
    serial_pub = Serial()

    try:
        rclpy.spin(serial_pub)

    except KeyboardInterrupt:
        serial_pub.get_logger().info('Serial connection stopped by KeyboardInterrupt')

    finally:
        serial_pub.destroy_node()
        rclpy.shutdown()
        serial_pub.get_logger().fatal('Serial Disconnected')

if __name__ == '__main__':
    main()
            