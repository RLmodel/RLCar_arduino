import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from std_msgs.msg import Bool

from enum import Enum, auto
from dataclasses import dataclass
from copy import deepcopy
from time import sleep

def isTrue(val: int)-> bool:
    return val == 1

class StateMachine(Enum):
    JOY = auto()
    LANE = auto()
    
@dataclass
class Xmode:
    left_updown: float = 0
    left_leftright: float = 0
    right_updown: float = 0
    right_leftright: float = 0
    
    btn_LB: bool = 0
    btn_RB: bool = 0

    btn_A: bool = 0
    btn_B: bool = 0

    btn_X: bool = 0
    btn_Y: bool = 0


class JoyToCmd(Node):
    def __init__(self):
        super().__init__("joy_to_cmd_vel_node")
        self.cmd_vel_pub = self.create_publisher(Twist, "cmd_vel", 10)
        # self.emergency_pub = self.create_publisher(Bool, "/emergency", 1)
        self.state_pub_ = self.create_publisher(Bool, "/state_machine", 1)

        # self.emergency_sub = self.create_subscription(Bool, "state", 1)
        self.joy_sub = self.create_subscription(Joy, "joy", self.sub_callback, 10)
        
        self.timer_ = self.create_timer(0.05, self.pub_twist_joy) # prevent arduino stop (serial buffer)
        self.twist = Twist()
        self.joy_keys = Xmode()
        self.prev_joy_keys = Xmode()
        self.emergency = Bool()
        self.state_msg = Bool()

        self.linear_speed_gain = 0.5
        self.angular_pose_gain = 2.0 # 50.0 * pi/180
        
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        self.max_linear_gain = 1.0

        self.state = StateMachine.JOY
        
    def __del__(self):
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        self.cmd_vel_pub.publish(self.twist)
        
    
    def sub_callback(self, data):
    # Joystick 은 "X" mode인 상태를 가정한다.
        # 왼쪽 스틱
        self.joy_keys.left_updown = data.axes[1]
        self.joy_keys.left_leftright = data.axes[0]
        
        # 오른쪽 스틱
        self.joy_keys.right_updown = data.axes[4]
        self.joy_keys.right_leftright= data.axes[3]

        # Linear Speed Up/Down
        self.joy_keys.btn_LB = isTrue(data.buttons[4])
        self.joy_keys.btn_RB = isTrue(data.buttons[5])

        # emergency && release
        self.joy_keys.btn_B = isTrue(data.buttons[1]) # B: emergency
        self.joy_keys.btn_A = isTrue(data.buttons[0]) # A: release

        self.joy_keys.btn_X = isTrue(data.buttons[2])
        self.joy_keys.btn_Y = isTrue(data.buttons[3])


        self.check_state()
        self.control_gain()
        self.prev_joy_keys = deepcopy(self.joy_keys) # shallow copy(copy.copy or A=B) cause error


    def check_state(self):
        
        if self.joy_keys.btn_X and not self.prev_joy_keys.btn_X:
            self.state = StateMachine.LANE
            self.state_msg.data = True
            self.state_pub_.publish(self.state_msg)
            self.get_logger().warn("STATE: lane detection")
            sleep(0.33) # for steady state

        elif self.joy_keys.btn_Y and not self.prev_joy_keys.btn_Y:
            self.state = StateMachine.JOY
            self.state_msg.data = False
            self.state_pub_.publish(self.state_msg)
            self.get_logger().warn("STATE: joystick control")
            sleep(0.33)
            
        else:
            pass


    def control_gain(self):

        if self.joy_keys.btn_LB and not self.prev_joy_keys.btn_LB:
            if self.linear_speed_gain <= 0:
                self.get_logger().warn("Min_speed is 0.0") 
            else:
                self.linear_speed_gain -= 0.125
                self.get_logger().info("Max_Speed : {0}".format(self.linear_speed_gain))
        
        if self.joy_keys.btn_RB and not self.prev_joy_keys.btn_RB:
            if self.linear_speed_gain >= self.max_linear_gain:
                self.get_logger().warn("Max_speed can't surpass 1.0") 
            else:
                self.linear_speed_gain += 0.125
                self.get_logger().info("Max_Speed : {0}".format(self.linear_speed_gain))

    def pub_twist_joy(self):
        
        self.twist.linear.x = self.joy_keys.left_updown* self.linear_speed_gain
        self.twist.linear.y = 0.0
        self.twist.linear.z = 0.0
        
        self.twist.angular.z = self.joy_keys.right_leftright* self.angular_pose_gain
        
        if self.state == StateMachine.JOY:
            self.cmd_vel_pub.publish(self.twist)
        else:
            pass

def main(args=None):
    rclpy.init(args=args)
    joy_to_cmd = JoyToCmd()
    rclpy.spin(joy_to_cmd)
    joy_to_cmd.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
