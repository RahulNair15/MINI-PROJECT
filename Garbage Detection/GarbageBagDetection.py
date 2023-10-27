import cv2
from ultralytics import YOLO
import supervision as sv
import numpy as np
import time

def main():
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) 
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    model = YOLO(r"C:\Users\a21ma\OneDrive\Desktop\Code\Projects\IITR Sociothon\IITR_Sociothon\models\GarbageBag.pt")
    
    box_annotator = sv.BoxAnnotator(
        thickness = 2,
        text_thickness = 2,
        text_scale = 1
    )
    
    excluded_classes = [25,24,23]
    
    while True:
        start_time = time.perf_counter()
        
        ret, frame = cap.read()
        
        result= model(frame)[0]
        
        detections = sv.Detections.from_yolov8(result)
        
        filtered_detections = [
            detection for detection in detections
            if detection[1] >=0.65 and detection[2] not in excluded_classes
        ]
        
        labels = [
            f"{model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, _ 
            in filtered_detections
        ]
        
        frame = box_annotator.annotate(scene=frame,detections=filtered_detections,labels=labels)
        
        end_time = time.perf_counter()
        fps = 1/ (end_time - start_time)
            
        cv2.putText(frame, f"FPS: {fps:.2f}",(20,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        
        if not ret: break
        cv2.imshow("yolov8",frame)
        
        # print(frame.shape)
        # break
        
        if cv2.waitKey(1) == 27 or cv2.getWindowProperty("yolov8", cv2.WND_PROP_VISIBLE) < 1:
            break
        
    # cap.release()
    # cv2.destroyAllWindows()
if __name__ == '__main__':
    main()