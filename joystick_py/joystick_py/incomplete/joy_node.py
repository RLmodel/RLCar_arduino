import rclpy.parameter
from sensor_msgs.msg import Joy
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time



class Joysub(Node):
    def __init__(self):
        super().__init__('joy_to_cmd')
        #self.declare_parameter('max_speed', 2)
        self.speed_weight = 1
        self.subscriber_ = self.create_subscription(Joy, 'joy', self.joy_callback, 10)
        self.publsiher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.msg_ = Twist()
        self.prev_LB = 0
        self.prev_RB = 0

    def joy_callback(self, data):
        #self.speed_weight = self.get_parameter('max_speed').value
        msg = self.msg_

        
        if data.buttons[4]==1 and self.prev_LB != 1:
            if self.speed_weight <= 0:
                self.get_logger().warn("min_speed is 0.0") 
            else:
                self.speed_weight -=0.5
                self.get_logger().info("Max_Speed : {0}".format(self.speed_weight))
            time.sleep(0.5)


        if data.buttons[5]==1 and self.prev_RB != 1:
            if self.speed_weight >= 3:
                self.get_logger().warn("max_speed can't surpass 3.0") 
            else:
                self.speed_weight +=0.5
                self.get_logger().info("Max_Speed : {0}".format(self.speed_weight))
            time.sleep(0.5)



        if data.axes[1] > 0:
             msg.linear.x = data.axes[1]*self.speed_weight

        elif data.axes[1] < 0:
            msg.linear.x = data.axes[1]*self.speed_weight

        else:
            msg.linear.x = 0.0

        if data.axes[3] < 0:
            msg.angular.z = data.axes[3]

        elif data.axes[3] > 0:
            msg.angular.z = data.axes[3]

        else:
            msg.angular.z = 0.0

        self.prev_LB = data.buttons[4]
        self.prev_RB = data.buttons[5]
        self.publsiher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    joynode = Joysub()
    rclpy.spin(joynode)
    joynode.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
