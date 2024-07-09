from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from dataclasses import dataclass

def isTrue(val: int)-> bool:
    return val == 1
    

@dataclass
class Xmode:
    left_updown: float = 0
    left_leftright: float = 0
    right_updown: float = 0
    right_leftright: float = 0
    
    btn_LB: bool = 0
    btn_RB: bool = 0


class JoyToCmd(Node):
    def __init__(self):
        super().__init__("joy_to_cmd_vel_node")
        self.cmd_vel_pub = self.create_publisher(Twist, "cmd_vel", 10)
        self.joy_sub = self.create_subscription(Joy, "joy", self.sub_callback, 10)

        self.twist = Twist()
        self.joy_keys = Xmode()
        self.prev_LB = 0
        self.prev_RB = 0


        self.linear_speed_gain = 0.5
        self.angular_pose_gain = 2.0
        

        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0

        
    
     
    def sub_callback(self, data):
    # Joystick 은 "X" mode인 상태를 가정한다.
        # 왼쪽 스틱
        self.joy_keys.left_updown = data.axes[1]
        self.joy_keys.left_leftright = data.axes[0]
        self.joy_keys.right_updown = data.axes[4]
        self.joy_keys.right_leftright= data.axes[3]


        # Linear Speed Up/Down
        self.joy_keys.btn_LB = isTrue(data.buttons[4])
        self.joy_keys.btn_RB = isTrue(data.buttons[5])


        self.pub_twist_joy()

        self.prev_LB = data.buttons[4]
        self.prev_RB = data.buttons[5]

    def pub_twist_joy(self):
        if self.joy_keys.btn_LB and not self.prev_LB:
            if self.linear_speed_gain <= 0:
                self.get_logger().warn("Min_speed is 0.0") 
            else:
                self.linear_speed_gain -= 0.125
                self.get_logger().info("Max_Speed : {0}".format(self.linear_speed_gain))
        
        if self.joy_keys.btn_RB and not self.prev_RB:
            if self.linear_speed_gain >= 3:
                self.get_logger().warn("Max_speed can't surpass 3.0") 
            else:
                self.linear_speed_gain += 0.125
                self.get_logger().info("Max_Speed : {0}".format(self.linear_speed_gain))

        self.twist.linear.x = self.joy_keys.left_updown* self.linear_speed_gain
        self.twist.linear.y = self.joy_keys.left_leftright
        self.twist.linear.z = 0.0

        self.twist.angular.z = self.joy_keys.right_leftright* self.angular_pose_gain


        self.cmd_vel_pub.publish(self.twist)

def main(args=None):
    rclpy.init(args=args)
    joy_to_cmd = JoyToCmd()
    rclpy.spin(joy_to_cmd)
    joy_to_cmd.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()