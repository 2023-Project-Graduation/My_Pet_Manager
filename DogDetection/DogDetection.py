import cv2
import numpy as np
import os
import timeit

# 웹캠 신호 받기
VideoSignal = cv2.VideoCapture(0)
VideoSignal.set(cv2.CAP_PROP_POS_MSEC, 60)

#캡쳐 프레임(6fps)
captured_num = 0
iscaptured = False


# YOLO 가중치 파일과 CFG 파일 로드
model_path = os.getcwd()+"/models/yolov2-tiny/"
print(model_path)
YOLO_net = cv2.dnn.readNet(model_path+"yolov2-tiny.weights",model_path+"yolov2-tiny.cfg")

# YOLO NETWORK 재구성
classes = []
with open("./DogDetection/yolo.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = YOLO_net.getLayerNames()
output_layers = [layer_names[i - 1] for i in YOLO_net.getUnconnectedOutLayers()]

while True:
    # 웹캠 프레임
    ret, frame = VideoSignal.read()
    h, w, c = frame.shape
    # print(VideoSignal.get(cv2.CAP_PROP_FPS))
    start_time = timeit.default_timer()

    # YOLO 입력
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0),
    True, crop=False)
    YOLO_net.setInput(blob)
    outs = YOLO_net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:

        for detection in out:
            captured_num = captured_num + 1
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
            #class_id == dog 
            if class_id == 16 and confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                dw = int(detection[2] * w)
                dh = int(detection[3] * h)
                # Rectangle coordinate
                x = int(center_x - dw / 2)
                y = int(center_y - dh / 2)
                boxes.append([x, y, dw, dh])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                #-- 검출된 객체 부분 자동 캡쳐
                if captured_num % 4 == 0: #-- 본인 편의에 맞게 프레임 설정할 것
                    img_crop = frame[y:y+dh, x:x+dw, :]
                    cv2.imwrite('img/image.png', img_crop) #-- 경로 설정
                    iscaptured = True
                    break



    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)

    if iscaptured:
        break


    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            score = confidences[i]

            # 경계상자와 클래스 정보 이미지에 입력
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
            cv2.putText(frame, label, (x, y - 20), cv2.FONT_ITALIC, 0.5,
            (255, 255, 255), 1)

    cv2.imshow("YOLOv3", frame)

    if iscaptured:
        break

    if cv2.waitKey(100) > 0:
        break

