## DINO-DETR

This section demonstrates an attempt on building a transformer-based object detector inspired by DETR and DINO. The model utilizes a self-supervised Vision Transformer (ViT) backbone (DINO ViT-S/8) for feature extraction and a DETR-style transformer head to directly predict object classes and bounding boxes, treating detection as a set prediction problem.

### Features

- **ViT Backbone**: Leverages pretrained DINO ViT-S/8 weights for robust image representation.
- **Transformer Detection Head**: Adapts a simplified DETR head for end-to-end object detection.
- **Set Prediction**: Predicts a fixed set of object queries, enabling direct class and bounding box prediction without anchors or proposals.
- **Jupyter Notebooks**: All code, experiments, and results are provided as Jupyter notebooks in the `DINO` directory.


