import os
import cv2
from ultralytics import YOLO

def crop_persons(image_path, person_boxes):
    image = cv2.imread(image_path)
    cropped_images = []
    for box in person_boxes:
        x1, y1, x2, y2 = map(int, box)
        cropped = image[y1:y2, x1:x2]
        cropped_images.append(cropped)
    return cropped_images

def prepare_ppe_dataset(person_det_model, input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for image_file in os.listdir(input_dir):
        if image_file.endswith(('.jpg', '.png', '.jpeg')):
            image_path = os.path.join(input_dir, image_file)
            results = person_det_model(image_path)
            person_boxes = results[0].boxes.xyxy.cpu().numpy()
            
            cropped_images = crop_persons(image_path, person_boxes)
            
            for i, cropped in enumerate(cropped_images):
                output_path = os.path.join(output_dir, f"{os.path.splitext(image_file)[0]}_person_{i}.jpg")
                cv2.imwrite(output_path, cropped)

def main():
    person_model = YOLO('path/to/person_detection_model.pt')
    input_dir = 'path/to/input/images'
    output_dir = 'path/to/output/cropped_persons'
    
    prepare_ppe_dataset(person_model, input_dir, output_dir)
    print(f"PPE dataset preparation completed. Cropped images saved in {output_dir}")

if __name__ == '__main__':
    main()
