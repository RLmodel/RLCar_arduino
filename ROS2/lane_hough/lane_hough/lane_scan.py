# Basic ROS 2 program to subscribe to real-time streaming 
# video from your built-in webcam
# Author:
# - RLmodel ybbaek
# - https://www.rlmodel.com
  
# Import the necessary libraries
import rclpy # Python library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
import numpy as np
from enum import Enum, auto

class StateMachine(Enum):
    JOY = auto()
    LANE = auto()

class ImageSubscriber(Node):
    
    def __init__(self):
        
        super().__init__('image_subscriber')
        self.br = CvBridge()
        
        self.declare_parameter("velocity", 0.5)
        self.velocity = self.get_parameter("velocity").get_parameter_value().double_value
        self.get_logger().info("cmd_vel : %2f" % self.velocity)
        self.declare_parameter("steering", 0.78)
        self.error_weight = self.get_parameter("steering").get_parameter_value().double_value
        self.get_logger().info("steering : %2f" % self.error_weight)
        
        self.declare_parameter("is_image_tools", True)
        is_image_tools = self.get_parameter("is_image_tools").get_parameter_value().bool_value
        
        if is_image_tools == True:
            self.subimg = self.create_subscription(Image, '/image', self.img_callback, 10)        #for image_tools
            self.get_logger().info('web_cam package : image_tools')
        else:
            self.subimg = self.create_subscription(Image,'/image_raw', self.img_callback, 10)    #for usb_cam
            self.get_logger().info('web_cam package : usb_cam')

        self.get_logger().info('Scan only detect a single point in front of it')
        self.subscan = self.create_subscription(LaserScan, '/scan', self.steering_callback, 10)
        self.steering = self.create_publisher(Twist, '/cmd_vel', 10)
        self.state_sub_ = self.create_subscription(Bool, '/state_machine', self.state_callback, 1)
        
        #timer_period = 1
        #self.timer = self.create_timer(timer_period, self.steering_callback)

        self.state = StateMachine.JOY
        self.steering
        self.error=0
        self.len_front=0

    def state_callback(self, data):
        
        if data.data == False:
            self.state = StateMachine.JOY
        
        else:
            self.state = StateMachine.LANE
    
    def img_callback(self, data):
        
        current_frame = self.br.imgmsg_to_cv2(data, desired_encoding='bgr8')
        gray = cv2.cvtColor(current_frame,1)
        result = process_frame(gray)
        cv2.imshow("camera", result) 
        cv2.waitKey(2)

        try:
            self.error = lnum-rnum  # left_line num - right_line num   #p
        except NameError:
            self.error = 0
            # self.get_logger().info("can't detect lane")
        
            
    def steering_callback(self, msg):
        if self.state == StateMachine.LANE:        
        
            
            self.len_front = msg.ranges[0]               # degree(0 ~ 359) == ranges[0 ~ 1079]
            
            error = self.error*self.error_weight                  #p
            twist_msg = Twist()
            #print(f'lnum = {error}')
            #print(f'rnum = {error}')
            print(f"front : {self.len_front}")
            
            if error > 4:
                
                if self.len_front > 0.5:                
                    #print(f' == right == :  {error}')
                    twist_msg.linear.x = self.velocity            #p
                    twist_msg.angular.z = -float(error)  
                    self.steering.publish(twist_msg)
                else:
                    twist_msg.linear.x = 0.0

                    self.steering.publish(twist_msg)
                    
            elif error < -4:
                                        #P
                if self.len_front > 0.5:
                    
                    #print(f' == left == :  {error}')
                    twist_msg.linear.x = self.velocity           #p
                    twist_msg.angular.z = -float(error)  
                    self.steering.publish(twist_msg)
                
                else:
                    twist_msg.linear.x = 0.0
                    self.steering.publish(twist_msg)

            else:     
                if self.len_front > 0.5:                           
                    #print(f' == straight == :  {error}')
                    twist_msg.linear.x = self.velocity            #p
                    twist_msg.angular.z = 0.0
                    self.steering.publish(twist_msg)
                
                else:
                    twist_msg.linear.x = 0.0
                    self.steering.publish(twist_msg)
        else:
            pass

        




    
def process_frame(frame):
    global height, width
    # 이미지 크기를 줄여 속도 향상
    
    
    #height, width = frame.shape[:2]
    #print(width, height)
    frame = cv2.resize(frame, (640, 480)) #2
    #frame = cv2.resize(frame, (width // 1, height // 1)) #2
    frame = frame[180:480, 0:640]
    # 이미지를 HSV로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 노란색 차선을 위한 HSV 범위 설정
    lower_yellow = np.array([20, 100, 100], dtype=np.uint8)
    upper_yellow = np.array([30, 255, 255], dtype=np.uint8)

    # 노란색 차선을 마스크로 추출
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # 차선을 찾기 위한 그레이 스케일 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 가우시안 블러 적용
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Canny 엣지 검출
    edges = cv2.Canny(blurred, 50, 150)
    
    # 노란색 차선과 엣지를 합친 이미지 생성
    combined = cv2.bitwise_or(edges, yellow_mask)

    # 허프 변환을 사용하여 선 감지
    lines = cv2.HoughLinesP(combined, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=100)

    # 차선이 없는 경우 처리
    if lines is None:
        print("No lanes detected")
        return frame

    # 차선 그리기
    else: 
        draw_lines(frame, lines)
        return frame

def draw_lines(frame, lines):
    # 왼쪽 차선과 오른쪽 차선을 구분하기 위한 리스트 초기화
    left_lines = []
    right_lines = []
    
    global rnum
    global lnum
    rnum = 0
    lnum = 0

    for line in lines:
        x1, y1, x2, y2 = line[0]
        slope = (y2 - y1) / (x2 - x1)

        # 기울기에 따라 왼쪽 또는 오른쪽 차선으로 분류
        if slope < 0: # openCV 카메라 좌표계는 Y축 아래 방향이 +이므로 slope가 음수값이면 우상향 직선이다.(왼쪽차선)
            if ( -5 < slope < -0.2 ):
                left_lines.append(line)
                lnum +=1
        else:
             if (0.2 <slope < 5):
                right_lines.append(line)
                rnum += 1
    #print('rnum :',rnum)
    #print('lnum : ',lnum)

    # 왼쪽 차선과 오른쪽 차선을 각각 그리기
    # draw_line_segments(frame, left_lines, color=(0, 255, 0))
    # draw_line_segments(frame, right_lines, color=(0, 0, 255))

    # 중앙선 계산 및 표시
    center_line = calculate_center_line(left_lines, right_lines)
    cv2.line(frame, center_line[0], center_line[1], (255, 255, 255), 2)

    # if lnum-rnum < -4:
    #     leftright = "Right"
    # elif lnum-rnum > 4:
    #     leftright = "Left"
    # else:
    #     leftright = "Straight"
    

    if lnum-rnum < -4:
        leftright = "LEFT"
    elif lnum-rnum > 4:
        leftright = "RIGHT"
    else:
        leftright = "Straight"

    
    # 픽셀 값 출력
    # pixel_value = calculate_pixel_value(frame, center_line)
    # cv2.putText(frame, f"Pixel Value: {pixel_value}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"Steer: {leftright}", (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 200, 100), 2)
    cv2.putText(frame, f"Left detected: {lnum}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 200), 2)
    cv2.putText(frame, f"Right detected: {rnum}", (400, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 100, 100), 2)

def draw_line_segments(frame, lines, color):
    for line in lines:
        x1, y1, x2, y2 = line[0]
        # cv2.line(frame, (x1, y1), (x2, y2), color, 2)

def calculate_center_line(left_lines, right_lines):
    # 왼쪽 차선과 오른쪽 차선의 끝점을 사용하여 중앙선 계산
    left_x = (np.mean([line[0][0] for line in left_lines]))
    left_y = (np.mean([line[0][1] for line in left_lines]))
    right_x = (np.mean([line[0][2] for line in right_lines]))
    right_y = (np.mean([line[0][3] for line in right_lines]))

    #print('left x ', left_x)
    #print('left y ',left_y)

    
    if ((np.isnan(left_x) == True) or (np.isnan(left_y) ==True) or (np.isnan(right_x) == True) or (np.isnan(left_y) == True)):
        
            center_line = ((385, 288), (208, 181)) # for prevent NaN  
            return center_line

    else:
       center_line = ((int(left_x), int(left_y)), (int(right_x), int(right_y))) 
       #print(center_line)    
       return center_line


def calculate_pixel_value(frame, center_line):
    # 중앙선 위의 픽셀 값 계산

    mid_x = (center_line[0][0] + center_line[1][0]) // 2
    mid_y = (center_line[0][1] + center_line[1][1]) // 2
    pixel_value = frame[mid_y, mid_x, 0]  # 블루 채널의 픽셀 값

    return pixel_value

def main(args=None):
    
    
    rclpy.init(args=args)
    detect = ImageSubscriber()


    try:
        rclpy.spin(detect)
    
    except KeyboardInterrupt:
        detect.get_logger().info('Stop detection')
    
    finally :
        detect.destroy_node()
        rclpy.shutdown()



if __name__ == '__main__':
    main()
