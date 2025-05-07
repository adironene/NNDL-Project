import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import sys

def inspect_tfrecord(tfrecord_path):

    feature_description = {
        'image/height': tf.io.FixedLenFeature([], tf.int64),
        'image/width': tf.io.FixedLenFeature([], tf.int64),
        'image/filename': tf.io.FixedLenFeature([], tf.string),
        'image/source_id': tf.io.FixedLenFeature([], tf.string),
        'image/encoded': tf.io.FixedLenFeature([], tf.string),
        'image/format': tf.io.FixedLenFeature([], tf.string),
        'image/object/bbox/xmin': tf.io.VarLenFeature(tf.float32),
        'image/object/bbox/xmax': tf.io.VarLenFeature(tf.float32),
        'image/object/bbox/ymin': tf.io.VarLenFeature(tf.float32),
        'image/object/bbox/ymax': tf.io.VarLenFeature(tf.float32),
        'image/object/class/text': tf.io.VarLenFeature(tf.string),
        'image/object/class/label': tf.io.VarLenFeature(tf.int64),
    }
    
    dataset = tf.data.TFRecordDataset(tfrecord_path)
    parsed_dataset = dataset.map(lambda example: tf.io.parse_single_example(
        example, feature_description))
    
    box_counts = []
    image_sizes = []
    class_distribution = {}
    
    print(f"Analyzing TFRecord file: {tfrecord_path}")
    print("=" * 20)
    
    count = 0
    for example in parsed_dataset:
        height = example['image/height'].numpy()
        width = example['image/width'].numpy()
        filename = example['image/filename'].numpy().decode('utf-8')
        
        xmins = tf.sparse.to_dense(example['image/object/bbox/xmin']).numpy()
        xmaxs = tf.sparse.to_dense(example['image/object/bbox/xmax']).numpy()
        ymins = tf.sparse.to_dense(example['image/object/bbox/ymin']).numpy()
        ymaxs = tf.sparse.to_dense(example['image/object/bbox/ymax']).numpy()
        
        class_labels = tf.sparse.to_dense(example['image/object/class/label']).numpy()
        class_texts = tf.sparse.to_dense(example['image/object/class/text']).numpy()
        
        for cls in class_labels:
            cls_key = int(cls)
            if cls_key in class_distribution:
                class_distribution[cls_key] += 1
            else:
                class_distribution[cls_key] = 1
        
        num_boxes = len(xmins)
        box_counts.append(num_boxes)
        image_sizes.append((height, width))
        
        if count < 5:
            print(f"Example {count+1}:")
            print(f"  Filename: {filename}")
            print(f"  Image size: {width}x{height}")
            print(f"  Number of boxes: {num_boxes}")
            
            class_count = {}
            for i, cls in enumerate(class_labels):
                cls_name = class_texts[i].decode('utf-8')
                if cls_name in class_count:
                    class_count[cls_name] += 1
                else:
                    class_count[cls_name] = 1
            print(f"  Classes: {class_count}")
            
            for i in range(min(3, num_boxes)):
                print(f"  Box {i+1}: [{xmins[i]:.4f}, {ymins[i]:.4f}, {xmaxs[i]:.4f}, {ymaxs[i]:.4f}], Class: {class_texts[i].decode('utf-8')}")
            print("-" * 40)
        
        count += 1
    
    print("\nDataset Summary:")
    print(f"Total number of examples: {count}")
    print(f"Average number of boxes per image: {np.mean(box_counts):.2f}")
    print(f"Min number of boxes: {np.min(box_counts)}")
    print(f"Max number of boxes: {np.max(box_counts)}")
    
    print("\nClass distribution:")
    for cls_id, count in class_distribution.items():
        print(f"  Class {cls_id}: {count} instances")
   
    return box_counts, image_sizes, class_distribution

def main():
    if len(sys.argv) < 2:
        print("Usage: include tf path as param")
        sys.exit(1)
    
    tfrecord_path = sys.argv[1]
    inspect_tfrecord(tfrecord_path)

if __name__ == "__main__":
    main()