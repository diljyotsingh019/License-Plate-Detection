from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.train(data = "data_ref.yaml", epochs = 100)