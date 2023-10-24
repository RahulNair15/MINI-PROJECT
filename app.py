from flask import Flask, render_template
from flask_socketio import SocketIO
import cv2
from ultralytics import YOLO
import supervision as sv
import base64
import io
import eventlet
import numpy as np
import time

# app = Flask(__name__)
# sockets = Sockets(app)

# model = None
# box_annotator = None
# # Initialize your machine learning model here
# # Replace 'your_model' with the actual code to load your model
# # You should have a function like load_model() or model.load() here
# # For simplicity, we'll create a placeholder function.

# def load_model():
#     # Replace this with code to load your model
#     # Example: model = tf.keras.models.load_model('your_model_path')
#     model = YOLO(r"C:\Users\a21ma\OneDrive\Desktop\IITR Sociothon\IITR_Sociothon\models\WasteSegregation.pt")
#     return model

# model = load_model()
# box_annotator = sv.BoxAnnotator(
#         thickness = 2,
#         text_thickness = 2,
#         text_scale = 1
#     )


# @app.route('/')
# def index():
#     return app.send_static_file('index.html')



app = Flask(__name__)
socketio = SocketIO(app)

box_annotator = None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    model = YOLO(r"C:\Users\a21ma\OneDrive\Desktop\IITR Sociothon\IITR_Sociothon\models\WasteSegregation.pt")  
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    def send_processed_frame():
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        excluded_classes = [25,24,23]
        
        while True:
            start_time = time.perf_counter()
            
            ret, frame = cap.read()
            
            result = model(frame, agnostic_nms=True)[0]
            
            detections = sv.Detections.from_yolov8(result)
            
            filtered_detections = [
                detection for detection in detections
                if detection[1] >=0.6 and detection[2] not in excluded_classes
            ]
            
            labels = [
                f"{model.model.names[class_id]} {confidence:0.2f}" for _, confidence, class_id, _ in filtered_detections
            ]
            
            frame = box_annotator.annotate(scene=frame, detections=filtered_detections, labels=labels)

            _, encoded_frame = cv2.imencode('.jpg', frame)
            frame_bytes = encoded_frame.tobytes()
            frame_base64 = base64.b64encode(frame_bytes).decode()
            socketio.emit('frame', frame_base64, broadcast=True)

            end_time = time.perf_counter()
            fps = 1 / (end_time - start_time)
            
            print(f"FPS: {fps:.2f}")

    eventlet.spawn(send_processed_frame)

if __name__ == '__main__':
    socketio.run(app, debug=True)

    
# Define an endpoint to receive the camera feed and return the classification result
# @app.route('/process_camera_feed', methods=['GET','POST'])
# def process_camera_feed():
#     try:
#         cap = cv2.VideoCapture(0)
#         cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) 
#         cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

#         if model is not None:
#             # Convert the frame to the format expected by your model
#             # You may need to resize, preprocess, or reshape the frame as needed
#             # Replace this with your actual preprocessing code
#             while True:
#                 start_time = time.perf_counter()
        
#                 ret, frame = cap.read()
        
#                 result= model(frame, agnostic_nms=True)[0]
                
#                 detections = sv.Detections.from_yolov8(result)
                        
#                 filtered_detections = [detection for detection in detections if detection[1] >=0.6]
                
#                 labels = [
#                     f"{model.model.names[class_id]} {confidence:0.2f}" for _, confidence, class_id, _ in filtered_detections
#                 ]
                
#                 frame = box_annotator.annotate(scene=frame,detections=filtered_detections,labels=labels)
                
#                 end_time = time.perf_counter()
#                 fps = 1/ (end_time - start_time)
                    
#                 cv2.putText(frame, f"FPS: {fps:.2f}",(20,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                
#                 if not ret: break
                
                    
#                 cv2.imshow("yolov8",frame)
#                 # print(frame.shape)
#                 # break
                
#                 if cv2.waitKey(1) == 27 or cv2.getWindowProperty("yolov8", cv2.WND_PROP_VISIBLE) < 1:
#                     break

#             # Return the result
#             return jsonify({'result': result.tolist()})
#         else:
#             return jsonify({'error': 'Model not loaded'})

#     except Exception as e:
#         return jsonify({'error': str(e)})

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)
