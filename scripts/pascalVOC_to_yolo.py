import argparse
import xml.etree.ElementTree as ET
import os
from pathlib import Path
import shutil

def convert_coordinates(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(input_path, output_path, classes):
    tree = ET.parse(input_path)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    with open(output_path, 'w') as out_file:
        for obj in root.iter('object'):
            difficult = obj.find('difficult')
            if difficult is not None:
                difficult = int(difficult.text)
            else:
                difficult = 0
            
            cls = obj.find('name').text
            if cls not in classes or difficult == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
                 float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = convert_coordinates((w, h), b)
            out_file.write(f"{cls_id} {' '.join([f'{a:.6f}' for a in bb])}\n")

def main():
    parser = argparse.ArgumentParser(description="Convert PascalVOC annotations to YOLO format")
    parser.add_argument("input_dir", help="Input directory containing PascalVOC annotations")
    parser.add_argument("output_dir", help="Output directory for YOLO annotations")
    parser.add_argument("--image_dir", help="Directory containing the image files", required=True)
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    image_dir = Path(args.image_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / 'labels').mkdir(parents=True, exist_ok=True)
    (output_dir / 'images').mkdir(parents=True, exist_ok=True)

    # Read classes from classes.txt
    classes_file = input_dir.parent / 'classes.txt'
    if not classes_file.exists():
        print(f"Error: classes.txt not found in {classes_file.parent}")
        return

    with open(classes_file, 'r') as f:
        classes = [line.strip() for line in f]

    # Process each XML file
    for xml_file in input_dir.glob('*.xml'):
        yolo_file = output_dir / 'labels' / f"{xml_file.stem}.txt"
        convert_annotation(xml_file, yolo_file, classes)
        print(f"Converted {xml_file.name} to {yolo_file.name}")

        # Copy corresponding image file
        image_file = image_dir / f"{xml_file.stem}.jpg"
        if image_file.exists():
            shutil.copy(image_file, output_dir / 'images' / image_file.name)
            print(f"Copied {image_file.name} to output directory")
        else:
            print(f"Warning: Image file {image_file.name} not found")

    print("Conversion completed successfully!")

if __name__ == "__main__":
    main()