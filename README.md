# Syook Assignment - PPE Detection

This project implements a Personal Protective Equipment (PPE) detection system using YOLOv8. It includes scripts for data preparation, dataset creation, and inference.

## Project Structure

```
Syook_Assignment/
│
├── config/
│   ├── person_data.yaml
│   └── ppe_data.yaml
│
├── scripts/
│   ├── pascalVOC_to_yolo.py
│   ├── prepare_ppe_dataset.py
│   └── inference.py
│
├── weights/
│   ├── person_detection.pt
│   └── ppe_detection.pt
│
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/charanbhatia/Syook_Assignment.git
   cd Syook_Assignment
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv myenv
   source myenv/bin/activate  # On Windows, use: myenv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### 1. Data Preparation

Convert PascalVOC annotations to YOLO format:

```
python scripts/pascalVOC_to_yolo.py --image_dir path/to/images path/to/input/annotations path/to/output/labels
```

### 2. Prepare PPE Dataset

Create a dataset for PPE detection from the person detection results:

```
python scripts/prepare_ppe_dataset.py path/to/person/images path/to/output/ppe_dataset weights/person_detection.pt
```

### 3. Inference

Run inference on images using the trained PPE detection model:

```
python scripts/inference.py path/to/input/images path/to/output/images weights/person_detection.pt weights/ppe_detection.pt
```

Note: The current implementation focuses on PPE detection, but the person detection model is kept for potential future use.

## Configuration

- `config/person_data.yaml`: Configuration for person detection model training
- `config/ppe_data.yaml`: Configuration for PPE detection model training

## Models

- `weights/person_detection.pt`: YOLOv8 model trained for person detection
- `weights/ppe_detection.pt`: YOLOv8 model trained for PPE detection

## Scripts

- `pascalVOC_to_yolo.py`: Converts PascalVOC format annotations to YOLO format
- `prepare_ppe_dataset.py`: Prepares the PPE dataset from person detection results
- `inference.py`: Performs inference on images using the trained PPE detection model

## Results

The inference results (images with bounding boxes) are saved in the specified output directory.

## Documentation

Google Doc Link: https://docs.google.com/document/d/1obGN5ry6vEWPDVYkYCA2s4W9B-j0jwJEKPSXYPYw9Yw/edit?usp=sharing

## Acknowledgments

- Ultralytics for the YOLOv8 implementation
- Syook for providing the assignment and dataset
