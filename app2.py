from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2
from ultralytics import YOLO
import supervision as sv
import base64
import io
import eventlet
import numpy as np
import time

app = Flask(__name__)
socketio = SocketIO(app)

box_annotator = None
is_processing = False  # A flag to track if processing is active

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

        excluded_classes = [25, 24, 23]

        while True:
            start_time = time.perf_counter()

            ret, frame = cap.read()

            if is_processing:  # Only process frames if the flag is True
                result = model(frame, agnostic_nms=True)[0]

                detections = sv.Detections.from_yolov8(result)

                filtered_detections = [
                    detection for detection in detections
                    if detection[1] >= 0.6 and detection[2] not in excluded_classes
                ]

                labels = [
                    f"{model.model.names[class_id]} {confidence:0.2f}" for _, confidence, class_id, _ in filtered_detections
                ]

                frame = box_annotator.annotate(scene=frame, detections=filtered_detections, labels=labels)

                _, encoded_frame = cv2.imencode('.jpg', frame)
                frame_bytes = encoded_frame.tobytes()
                frame_base64 = base64.b64encode(frame_bytes).decode()
                socketio.emit('frame', frame_base64)

            end_time = time.perf_counter()
            fps = 1 / (end_time - start_time)

            print(f"FPS: {fps:.2f}")

    eventlet.spawn(send_processed_frame)

# Define a Socket.IO event to start processing
@socketio.on('start_processing')
def start_processing():
    global is_processing
    is_processing = True

# Define a Socket.IO event to stop processing
@socketio.on('stop_processing')
def stop_processing():
    global is_processing
    is_processing = False

if __name__ == '__main__':
    socketio.run(app, debug=True)