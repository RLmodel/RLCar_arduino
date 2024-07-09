# Basic ROS 2 program to subscribe to real-time streaming 
# video from your built-in webcam
# Author:
# - RLmodel ybbaek
# - https://www.rlmodel.com
  
# Import the necessary libraries
import rclpy # Python library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
import numpy as np
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time


class ImageSubscriber(Node):
    
    def __init__(self):
        
        super().__init__('image_subscriber')
        self.br = CvBridge()
        self.subimg = self.create_subscription(Image, '/image', self.img_callback, 10)        #for image_tools
        #self.subimg = self.create_subscription(Image,'/image_raw', self.img_callback, 10)    #for usb_cam
        
        self.subscan = self.create_subscription(LaserScan, '/scan', self.steering_callback, 10)
        self.steering = self.create_publisher(Twist, '/cmd_vel', 10)
        
        #timer_period = 1   #p
        #self.timer = self.create_timer(timer_period, self.steering_callback)

        #self.subscan
        self.steering
        self.error=0
    
    def img_callback(self, data):
        
        current_frame = self.br.imgmsg_to_cv2(data, desired_encoding='bgr8')
        gray = cv2.cvtColor(current_frame,1)
        result = process_frame(gray)
        cv2.imshow("camera", result) 
        cv2.waitKey(2)
        
        self.error = lnum-rnum  # left_line num - right_line num   #p
        

    def steering_callback(self, msg):
        len_front = msg.ranges[0]               # degree(0 ~ 359) == ranges[0 ~ 1079] CCW
        len_left15 = msg.ranges[45]              # 15 degree (left)  
        len_right15 = msg.ranges[1035]           # 15 degree (right)
   
        error = self.error*0.78                      #p
        twist_msg = Twist()
        #print(f'lnum = {error}')
        #print(f'rnum = {error}')
        print(f"left : {len_left15}")
        print(f"front : {len_front}")
        print(f"right : {len_right15}")
        #print(msg.ranges[0:45] + msg.ranges[1035:1079])      
        if error > 4:                                #p
            if  all(value > 0.5 for value in msg.ranges[0:45] + msg.ranges[1035:1079]):                
                #print(f' == right == :  {error}')
                twist_msg.linear.x = 0.35            #p
                twist_msg.angular.z = float(error)  
                self.steering.publish(twist_msg)
            else:
                twist_msg.linear.x = 0.0
        
                self.steering.publish(twist_msg)
                
        

        elif error < -4:                             #p         
            if  all(value > 0.5 for value in msg.ranges[0:45] + msg.ranges[1035:1079]):   
            
                #print(f' == left == :  {error}')
                twist_msg.linear.x = 0.35            #p
                twist_msg.angular.z = float(error)  
                self.steering.publish(twist_msg)
            
            else:
                twist_msg.linear.x = 0.0
                self.steering.publish(twist_msg)

        else:     
            if  all(value > 0.5 for value in msg.ranges[0:45] + msg.ranges[1035:1079]):                           
                #print(f' == straight == :  {error}')
                twist_msg.linear.x = 0.35            #p
                twist_msg.angular.z = 0.0
                self.steering.publish(twist_msg)
            
            else:
                twist_msg.linear.x = 0.0
                self.steering.publish(twist_msg)

        #time.sleep(1)

        




    
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
        if slope < 0:
            if ( -5< slope < -0.2 ):
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

    # 픽셀 값 출력
    pixel_value = calculate_pixel_value(frame, center_line)
    cv2.putText(frame, f"Pixel Value: {pixel_value}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

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
