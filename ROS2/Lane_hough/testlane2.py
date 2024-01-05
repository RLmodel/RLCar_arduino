import cv2
import numpy as np

def find_yellow_lane(frame):
    # 이미지 크기를 줄여 속도 향상
    height, width = frame.shape[:2]
    frame = cv2.resize(frame, (width // 2, height // 2))

    # 이미지를 HSV로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 노란색 차선을 위한 HSV 범위 설정
    lower_yellow = np.array([20, 100, 100], dtype=np.uint8)
    upper_yellow = np.array([30, 255, 255], dtype=np.uint8)

    # 노란색 차선을 마스크로 추출
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    return yellow_mask

def sliding_window(image, n_windows=9, margin=100, minpix=50):
    histogram = np.sum(image[image.shape[0]//2:, :], axis=0)
    out_img = np.dstack((image, image, image))*255
    midpoint = histogram.shape[0] // 2
    leftx_base = np.argmax(histogram[:midpoint])
    rightx_base = np.argmax(histogram[midpoint:]) + midpoint

    window_height = image.shape[0] // n_windows
    nonzero = image.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])
    leftx_current = leftx_base
    rightx_current = rightx_base

    left_lane_inds = []
    right_lane_inds = []

    for window in range(n_windows):
        win_y_low = image.shape[0] - (window + 1) * window_height
        win_y_high = image.shape[0] - window * window_height
        win_xleft_low = leftx_current - margin
        win_xleft_high = leftx_current + margin
        win_xright_low = rightx_current - margin
        win_xright_high = rightx_current + margin

        good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & 
                          (nonzerox >= win_xleft_low) & (nonzerox < win_xleft_high)).nonzero()[0]
        good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & 
                           (nonzerox >= win_xright_low) & (nonzerox < win_xright_high)).nonzero()[0]

        left_lane_inds.append(good_left_inds)
        right_lane_inds.append(good_right_inds)

        if len(good_left_inds) > minpix:
            leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
        if len(good_right_inds) > minpix:        
            rightx_current = np.int(np.mean(nonzerox[good_right_inds]))

    left_lane_inds = np.concatenate(left_lane_inds)
    right_lane_inds = np.concatenate(right_lane_inds)

    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds] 
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds]

    return leftx, lefty, rightx, righty

def fit_polynomial(image, leftx, lefty, rightx, righty):
    left_fit = np.polyfit(lefty, leftx, 2)
    right_fit = np.polyfit(righty, rightx, 2)

    ploty = np.linspace(0, image.shape[0]-1, image.shape[0])
    left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
    right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]

    return left_fitx, right_fitx, ploty

def draw_lane(frame, left_fitx, right_fitx, ploty):
    warp_zero = np.zeros_like(frame).astype(np.uint8)
    color_warp = np.dstack((warp_zero, warp_zero, warp_zero))

    pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
    pts = np.hstack((pts_left, pts_right))

    cv2.fillPoly(color_warp, np.int_([pts]), (0, 0, 255))

    result = cv2.addWeighted(frame, 1, color_warp, 0.3, 0)

    return result

def calculate_center_offset(image, left_fitx, right_fitx):
    lane_width_pixels = right_fitx[-1] - left_fitx[-1]
    midpoint_pixels = lane_width_pixels / 2 + left_fitx[-1]

    center_offset_pixels = image.shape[1] / 2 - midpoint_pixels

    return center_offset_pixels

def process_frame(frame):
    yellow_mask = find_yellow_lane(frame)

    # sliding window를 사용하여 차선 좌표 찾기
    leftx, lefty, rightx, righty = sliding_window(yellow_mask)

    # 2차 다항식으로 차선 피팅
    left_fitx, right_fitx, ploty = fit_polynomial(yellow_mask, leftx, lefty, rightx, righty)

    # 차선 그리기
    result = draw_lane(frame, left_fitx, right_fitx, ploty)

    # 중앙선 계산 및 표시
    center_offset_pixels = calculate_center_offset(frame, left_fitx, right_fitx)
    cv2.line(result, (int(frame.shape[1] / 2), 0), (int(frame.shape[1] / 2), frame.shape[0]), (0, 0, 255), 2)
    cv2.line(result, (int(left_fitx[-1]), frame.shape[0]), (int(right_fitx[-1]), frame.shape[0]), (255, 0, 0), 2)

    # 픽셀 값 출력
    cv2.putText(result, f"Center Offset: {center_offset_pixels:.2f} pixels", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    return result

def main():
    cap = cv2.VideoCapture(2)  # 카메라 장치 번호에 따라 변경 가능

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            print("Error reading frame")
            continue

        try:
            processed_frame = process_frame(frame)
            cv2.imshow("Lane Detection", processed_frame)
        except Exception as e:
            print(f"Error processing frame: {e}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
