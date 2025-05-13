import os
import csv
import shutil

class GenerateInputData:

    def __init__(self):
        pass

    def createDatasetDirs(self):
        os.makedirs("dataset/images/train", exist_ok=True)
        os.makedirs("dataset/images/val", exist_ok=True)
        os.makedirs("dataset/images/test", exist_ok=True)

        os.makedirs("dataset/labels/train", exist_ok=True)
        os.makedirs("dataset/labels/val", exist_ok=True)
        os.makedirs("dataset/labels/test", exist_ok=True)
    
    def mapImagesToLabels(self, path):
        image_to_label = {}
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['filename'] in image_to_label:
                    image_to_label[row['filename']].append([row['width'], row['height'], row['class'], row['xmin'], row['ymin'], row['xmax'], row['ymax']])
                else:
                    image_to_label[row['filename']] = []
                    image_to_label[row['filename']].append([row['width'], row['height'], row['class'], row['xmin'], row['ymin'], row['xmax'], row['ymax']])

        return image_to_label

    def addFilesToDatasetDirs(self, src_images_dir, dest_images_dir, dest_labels_dir, imageToLabelDict):
        os.makedirs(dest_images_dir, exist_ok=True)
        for filename in os.listdir(src_images_dir):
            if filename == "_annotations.csv":
                continue
            listLabels = imageToLabelDict[filename]
            name, _ = os.path.splitext(filename)
            labelsFilename = f"{name}.txt"
            labelsFilePath = os.path.join(dest_labels_dir, labelsFilename)
            for width, height, label_class, xmin, ymin, xmax, ymax in listLabels:
                with open(labelsFilePath, "a") as f:
                    classLabel = "0" if label_class == "enemy" else "1"
                    x_center = str(round(((float(xmin) + float(xmax)) / 2) / (float(width)), 3))
                    y_center = str(round(((float(ymin) + float(ymax)) / 2) / (float(height)), 3))
                    box_width = str(round((float(xmax) - float(xmin)) / (float(width)), 3))
                    box_height = str(round((float(ymax) - float(ymin)) / (float(height)), 3))
                    f.write(classLabel + " " + x_center + " " + y_center + " " + box_width + " " + box_height + "\n")

            src_path = os.path.join(src_images_dir, filename)
            dst_path = os.path.join(dest_images_dir, filename)
            shutil.copy(src_path, dst_path)

def main():
    gd = GenerateInputData()
    gd.createDatasetDirs()
    train_dict = gd.mapImagesToLabels("../data/train/_annotations.csv")
    val_dict = gd.mapImagesToLabels("../data/valid/_annotations.csv")
    test_dict = gd.mapImagesToLabels("../data/test/_annotations.csv")

    gd.addFilesToDatasetDirs(src_images_dir="../data/valid/", dest_images_dir="dataset/images/val/", dest_labels_dir="dataset/labels/val/", imageToLabelDict=val_dict)
    gd.addFilesToDatasetDirs(src_images_dir="../data/train/", dest_images_dir="dataset/images/train/", dest_labels_dir="dataset/labels/train/", imageToLabelDict=train_dict)
    gd.addFilesToDatasetDirs(src_images_dir="../data/test/", dest_images_dir="dataset/images/test/", dest_labels_dir="dataset/labels/test/", imageToLabelDict=test_dict)


if __name__ == "__main__":
    main()