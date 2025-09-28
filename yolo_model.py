# yolo_model.py
from ultralytics import YOLO
from PIL import Image
import io

# Load your custom-trained YOLO model
model = YOLO('best.pt') 

def run_yolo_detection(image_bytes: bytes) -> dict:
    """
    Takes image bytes, runs YOLO detection, and returns a dictionary
    mapping the detected class name (e.g., 'top-wear') to its cropped PIL image.
    """
    image = Image.open(io.BytesIO(image_bytes))
    
    # Run detection
    results = model(image)
    
    detected_items = {}
    # Loop through the detected boxes
    for result in results:
        # Get the mapping of class index to class name (e.g., 0: 'top-wear')
        class_names = result.names
        for box in result.boxes:
            # Get the detected class index and name
            class_index = int(box.cls[0])
            detected_class_name = class_names[class_index]
            
            # Get bounding box coordinates
            xyxy = box.xyxy[0].tolist()
            
            # Crop the image
            cropped_img = image.crop(xyxy)
            
            # Store it in the dictionary
            detected_items[detected_class_name] = cropped_img
            
    return detected_items
