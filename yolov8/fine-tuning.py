from ultralytics import YOLO

model = YOLO('yolov8n.pt')

model.train(
    data='./yolov8.yaml',
    epochs=50,
    imgsz=416,
    batch=16,
    name='valorant-finetune',
    patience=10,
    verbose=True
)