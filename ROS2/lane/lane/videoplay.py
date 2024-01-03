import cv2


cap = cv2.VideoCapture('/home/rlmodel/ros2_ws/hello2.avi')
w=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(w)
print(h)

while True:
    _, frame = cap.read()
    cv2.imshow('test', frame)
    if cv2.waitKey(40) == 27:
        cv2.waitKey(0)

    

