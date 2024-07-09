#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import cv2
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
import numpy as np



Width = 640
Height = 480

window_title = 'Lane_detection'

warp_img_w = 640
warp_img_h = 480

warpx_margin = 10
warpy_margin = 3

nwindows = 10         #number of windows
margin = 12
minpix = 5

lane_bin_th = 100     #threshold parameter

warp_src  = np.array([
    [230-warpx_margin, 200-warpy_margin],  
    [45-warpx_margin,  450+warpy_margin],
    [445+warpx_margin, 200-warpy_margin],
    [610+warpx_margin, 450+warpy_margin]
    ], dtype=np.float32)

warp_dist = np.array([
            [0,0],
            [0,warp_img_h],
            [warp_img_w,0],
            [warp_img_w, warp_img_h]
            ], dtype=np.float32)

calibrated = True
if calibrated:
    mtx = np.array([
    [1445.058890, 0.0, 960.000000], 
    [0.0, 1445.058890, 540.000000], 
    [0.0, 0.0, 1.0]
    ])
    dist = np.array([-0.545321, 0.866339, 0.003466, -0.003516, 0.0])
    cal_mtx, cal_roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (Width, Height), 1, (Width, Height))

class Lane(Node):

    def __init__(self):
        super().__init__('Lane')

        
        #self.subimg = self.create_subscription(Image,'/image', self.img_callback, 10)       #for image_tools
        self.subimg = self.create_subscription(Image,'/image_raw', self.img_callback, 10)    #for usb_cam
        self.bridge = CvBridge()
        self.img = None
        
        self.steering = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 1
        self.timer = self.create_timer(timer_period, self.steering_callback)
        self.Sx = 0
        self.err = 0

        self.get_logger().info('==== Lane_detection Started ====\n')
        

    def img_callback(self, data):
        
        self.img = self.bridge.imgmsg_to_cv2(data, desired_encoding='bgr8')
        frame = self.img 
        image = calibrate_image(frame)
        warp_img, M, Minv = warp_image(image, warp_src, warp_dist, (warp_img_w, warp_img_h))
        left_fit, right_fit = warp_process_image(warp_img)
        lane_img = draw_lane(image, warp_img, Minv, left_fit, right_fit)
        
        self.Sx = point2 - point1
        self.err = self.Sx/10               #set error for steering
                              
        
        #writer.write(lane_img)  # 프레임 저장
        cv2.imshow(window_title, lane_img) 
        cv2.waitKey(2)
        

    def steering_callback(self):
        
        Sx = self.Sx
        err = self.err
        print(f'Sx : {Sx}')
        #print(f'left  : {leftx_current}')
        #print(f'right : {rightx_current}')
        twist_msg = Twist()
        
        if Sx > 4:
            self.get_logger().info(f'==== right ==== : {err}')
            twist_msg.linear.x = 0.3
            twist_msg.angular.z = float(err)
            self.steering.publish(twist_msg)
            #print(twist_msg)
            
        elif Sx < -4:
            self.get_logger().info(f'==== left ==== : {err}')
            twist_msg.linear.x = 0.3
            twist_msg.angular.z = float(err)
            self.steering.publish(twist_msg) 
            #print(twist_msg)
            
        else:
            self.get_logger().info(f'==== straight ==== : {err}')
            twist_msg.linear.x = 0.5
            twist_msg.angular.z = 0.0
            self.steering.publish(twist_msg)
            #print(twist_msg)
            
        print('\n')


def calibrate_image(frame):
    global Width, Height
    global mtx, dist
    global cal_mtx, cal_roi
    
    tf_image = cv2.undistort(frame, mtx, dist, None, cal_mtx)
    x, y, w, h = cal_roi
    tf_image = tf_image[y:y+h, x:x+w]

    return cv2.resize(tf_image, (Width, Height))

def warp_image(img, src, dst, size):
    M = cv2.getPerspectiveTransform(src, dst)
    Minv = cv2.getPerspectiveTransform(dst, src)
    warp_img = cv2.warpPerspective(img, M, size, flags=cv2.INTER_LINEAR)

    return warp_img, M, Minv

def warp_process_image(img):
    global nwindows
    global margin
    global minpix
    global lane_bin_th
    global leftx_current
    global rightx_current

    blur = cv2.GaussianBlur(img,(5, 5), 0)
    _, L, _ = cv2.split(cv2.cvtColor(blur, cv2.COLOR_BGR2HLS))
    _, lane = cv2.threshold(L, lane_bin_th, 255, cv2.THRESH_BINARY)

    
    histogram = np.sum(lane[lane.shape[0]//2:,:], axis=0)      
    midpoint = np.int(histogram.shape[0]/2)
    leftx_current = np.argmax(histogram[:midpoint])
    rightx_current = np.argmax(histogram[midpoint:]) + midpoint
    window_height = np.int(lane.shape[0]/nwindows)
    nz = lane.nonzero()

    left_lane_inds = []
    right_lane_inds = []
    
    lx, ly, rx, ry = [], [], [], []

    out_img = np.dstack((lane, lane, lane))*255

    for window in range(nwindows):

        win_yl = lane.shape[0] - (window+1)*window_height
        win_yh = lane.shape[0] - window*window_height

        win_xll = leftx_current - margin
        win_xlh = leftx_current + margin
        win_xrl = rightx_current - margin
        win_xrh = rightx_current + margin

        cv2.rectangle(out_img,(win_xll,win_yl),(win_xlh,win_yh),(0,255,0), 2) 
        cv2.rectangle(out_img,(win_xrl,win_yl),(win_xrh,win_yh),(0,255,0), 2) 

        good_left_inds = ((nz[0] >= win_yl)&(nz[0] < win_yh)&(nz[1] >= win_xll)&(nz[1] < win_xlh)).nonzero()[0]
        good_right_inds = ((nz[0] >= win_yl)&(nz[0] < win_yh)&(nz[1] >= win_xrl)&(nz[1] < win_xrh)).nonzero()[0]

        left_lane_inds.append(good_left_inds)
        right_lane_inds.append(good_right_inds)

        if len(good_left_inds) > minpix:
            leftx_current = np.int(np.mean(nz[1][good_left_inds]))
        if len(good_right_inds) > minpix:        
            rightx_current = np.int(np.mean(nz[1][good_right_inds]))

        lx.append(leftx_current)
        ly.append((win_yl + win_yh)/2)

        rx.append(rightx_current)
        ry.append((win_yl + win_yh)/2)
    
    global point1
    global point2
    point1 = (lx[2] + rx[2])/2
    point2 = (lx[7] + rx[7])/2
    #print(point1)
    #print(point2)

    left_lane_inds = np.concatenate(left_lane_inds)
    right_lane_inds = np.concatenate(right_lane_inds)


    lfit = np.polyfit(np.array(ly),np.array(lx),2)
    rfit = np.polyfit(np.array(ry),np.array(rx),2)

    #print(f'lfit = {lfit}')
    #print(f'rfit = {rfit}')


    out_img[nz[0][left_lane_inds], nz[1][left_lane_inds]] = [0, 255, 0]
    out_img[nz[0][right_lane_inds] , nz[1][right_lane_inds]] = [0, 255, 0]
    cv2.imshow("Bird Eye View", out_img)

    return lfit, rfit

def draw_lane(image, warp_img, Minv, left_fit, right_fit):
    global Width, Height
    yMax = warp_img.shape[0]
    ploty = np.linspace(0, yMax - 1, yMax)
    color_warp = np.zeros_like(warp_img).astype(np.uint8)
    
    left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
    right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]
    pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))]) 
    pts = np.hstack((pts_left, pts_right))
    
    color_warp = cv2.fillPoly(color_warp, np.int_([pts]), (0, 255, 0))
    newwarp = cv2.warpPerspective(color_warp, Minv, (Width, Height))

   

    return cv2.addWeighted(image, 1, newwarp, 0.3, 0)



#fourcc = cv2.VideoWriter_fourcc(*'XVID')   # 영상 저장을 위한 VideoWriter 인스턴스 생성
#writer = cv2.VideoWriter('hello.avi', fourcc, 24, (int(Width), int(Height)))
                  
def main(args=None):
    global Width, Height
    
    rclpy.init(args=args)
    detect = Lane()

    try:
        rclpy.spin(detect)
    
    except KeyboardInterrupt:
        detect.get_logger().info('Stop detection')
    
    finally :
        detect.destroy_node()
        rclpy.shutdown()



if __name__ == '__main__':
    main()
