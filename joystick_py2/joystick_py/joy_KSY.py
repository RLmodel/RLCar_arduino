from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32
from std_msgs.msg import UInt8
from dataclasses import dataclass

def isTrue(val: int)-> bool:
    #print("debugging")
    return val == 1
    

#@dataclass
class Xmode:
    left_updown: float = 0
    left_leftright: float = 0
    right_updown: float = 0
    right_leftright: float = 0

    btn_updown: int = 0
    btn_leftright: int = 0

    btn_a: bool = 0
    btn_b: bool = 0
    btn_x: bool = 0
    btn_y: bool = 0
    
    btn_LB: bool = 0
    btn_RB: bool = 0
    btn_back: bool = 0
    btn_start: bool = 0


class JoyToCmd(Node):
    def __init__(self):
        super().__init__("joy_to_cmd_vel_node")
        self.cmd_vel_pub = self.create_publisher(Twist, "cmd_vel", 5)
        self.src_mode_pub = self.create_publisher(UInt8, "src_mode", 5)
        self.accel_pub = self.create_publisher(Float32, "accel_vel", 5)
        self.joy_sub = self.create_subscription(Joy, "joy", self.sub_callback, 10)

        self.twist = Twist()
        self.src_mode = UInt8()
        self.accel = Float32()

        self.prev_joy_keys = Xmode()
        self.joy_keys = Xmode()
        
        self.linear_speed_gain = 0.5
        self.angular_pose_gain = 2.0
        self.btn_control_gain = 0.0625

        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0

        self.accel.data = 5.0
        self.src_mode.data = 1
    
     
    def sub_callback(self, data):
    # Joystick 은 "X" mode인 상태를 가정한다.
        # 왼쪽 스틱
        self.joy_keys.left_updown = data.axes[1]
        self.joy_keys.left_leftright = data.axes[0]
        self.joy_keys.right_updown = data.axes[4]
        self.joy_keys.right_leftright= data.axes[3]

        # 십자 버튼
        self.joy_keys.btn_updown = data.axes[7]     # +1 btn up / -1 btn down
        self.joy_keys.btn_leftright = data.axes[6]  # +1 btn left / -1 btn right

    # mode change
        # A mode = joycontrol mode
        self.joy_keys.btn_a = isTrue(data.buttons[0])
        # A mode = joycontrol mode
        self.joy_keys.btn_b = isTrue(data.buttons[1])

        self.joy_keys.btn_x = isTrue(data.buttons[2])
        self.joy_keys.btn_y = isTrue(data.buttons[3])

        # Linear Speed Up/Down
        self.joy_keys.btn_LB = data.buttons[4]
        self.joy_keys.btn_RB = data.buttons[5]

        self.joy_keys.btn_back = isTrue(data.buttons[6])
        self.joy_keys.btn_start = isTrue(data.buttons[7])

        # if self.joy_keys.btn_a == 1.0 and self.prev_joy_keys.btn_a == 0.0:
        #     pass        
        # if self.joy_keys.btn_b == 1.0 and self.prev_joy_keys.btn_b == 0.0:
        #     pass
        
        self.pub_twist_joy()

        #self.prev_joy_keys = self.joy_keys

    def pub_twist_joy(self):
        
        if self.joy_keys.btn_LB==True and self.prev_joy_keys.btn_LB != True:
            self.linear_speed_gain -= 0.125
            self.get_logger().info("Max_Speed : {0}".format(self.linear_speed_gain))
        if self.joy_keys.btn_RB and not self.prev_joy_keys.btn_RB:
            self.linear_speed_gain += 0.125
            self.get_logger().info("Max_Speed : {0}".format(self.linear_speed_gain))

        self.twist.linear.x = self.joy_keys.left_updown* self.linear_speed_gain
        self.twist.linear.y = self.joy_keys.left_leftright
        self.twist.linear.z = 0.0
        
        self.twist.angular.z = self.joy_keys.right_leftright* self.angular_pose_gain

        self.prev_joy_keys = self.joy_keys
        self.cmd_vel_pub.publish(self.twist)

def main(args=None):
    rclpy.init(args=args)
    joy_to_cmd = JoyToCmd()
    rclpy.spin(joy_to_cmd)
    joy_to_cmd.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()