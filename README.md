# NNDL-Project

## Tensorflow

Dependencies needed
```
pip install tensorflow
pip install tf-slim
pip install opencv-python
pip install lxml
pip install Cython
pip install contextlib2
pip install pillow
pip install pycocotools
pip install matplotlib

```

Clone TF object detection API
```
git clone https://github.com/tensorflow/models.git
cd models/research
# Compile protobufs
protoc object_detection/protos/*.proto --python_out=.
# Add to PYTHONPATH
set PYTHONPATH=%cd%;%cd%\slim
```

download model from tf model zoo

https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md
```centernet_mobilenetv2fpn_512x512_coco17_od.tar```