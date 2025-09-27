from ultralytics import YOLO
from PIL import Image
import io

# Load your custom-trained YOLO model
model = YOLO('best.pt') 

def run_yolo_detection(uploaded_image):
    """
    Takes a user-uploaded image, runs YOLO detection, and returns cropped images.
    """
    # Read the image from the uploaded file
    image_bytes = uploaded_image.getvalue()
    image = Image.open(io.BytesIO(image_bytes))
    
    # Run detection
    results = model(image)
    
    cropped_images = []
    # Loop through the detected boxes
    for result in results:
        for box in result.boxes:
            # Get the coordinates of the bounding box
            xyxy = box.xyxy[0].tolist()
            # Crop the image using the bounding box coordinates
            cropped_img = image.crop(xyxy)
            cropped_images.append(cropped_img)
            
    return cropped_images