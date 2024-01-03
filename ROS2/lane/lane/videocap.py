import cv2

cap=cv2.VideoCapture(0)

w=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

print(w,h)

while True:
    
    _, frame = cap.read()
    reframe = cv2.resize(frame,(640, 480), interpolation=cv2.INTER_AREA)
    print(reframe.shape)
    cv2.imshow('frame' , reframe)
    cv2.waitKey(20)