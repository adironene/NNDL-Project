import os
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import sys
import cv2
import time
import argparse

MODEL_PATH = ""
IMAGE_HEIGHT = 640
IMAGE_WIDTH = 640

class ValorantDetector:
    def __init__(self, model_path = MODEL_PATH):
        self.model = tf.keras.models.load_model(model_path, compile= False)

        self.class_map = {
            0: 'background',
            1: 'enemy',
            2: 'enemy_head'
        }

        self.colors = {
            'background': (200, 200, 200),
            'enemy': (0, 0, 200),
            'enemy_head': (200, 0, 0)
        }

    
    def preprocess_img(self, image):
        if isinstance(image, str):
            image = cv2.imread(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        input_img = cv2.resize(image, (IMAGE_WIDTH, IMAGE_HEIGHT))
        input_tensor = input_img.astype(np.float32) / 255.0
        input_tensor = np.expand_dims(input_tensor, axis=0)

        return input_tensor, image
    
    def detect(self, image, confidence_threshold=0.5):
        input_tensor, original_image = self.preprocess_img(image)
        start_t = time.time()
        predictions = self.model(input_tensor)
        total_time = time.time() - start_t

        boxes = predictions['boxes'][0].numpy()
        scores = tf.reduce_max(predictions['classes'][0], axis=-1).numpy()

        return [], image, total_time


    def main():
        parser = argparse.ArgumentParser(description='Val Enemy Detector')
        parser.add_argument('--model', type=str, default=MODEL_PATH)
        parser.add_argument('--input', type=str, default=None)
        parser.add_argument('--output', type=str, default=None, help='path to save output')
        parser.add_argument('--confidence', type=float, default=0.5)
        args = parser.parse_args()

        detector_model = ValorantDetector(model_path=args.model)
        if not args.input:
            print('Error: Input path required')
            return
        detections, image, inference_time = detector_model.detect(args.input, args.confidence)
        print(f"detected {len(detections)} objects in {inference_time} seconds")
    if __name__ == "__main__":
        main()
