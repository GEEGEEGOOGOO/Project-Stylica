# main.py (Your new backend file)
from fastapi import FastAPI, UploadFile, File
import uvicorn
import os
import google.generativeai as genai

# Import the functions you've already written in your other files
from yolo_model import load_yolo_model, run_yolo_on_image 
from beit_model import load_beit_model, run_beit_on_image

# --- 1. INITIALIZATION ---
app = FastAPI(title="Stylia AI Engine")

# Load your API Key securely
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Load your models once when the server starts
print("Loading YOLO model...")
yolo_model = load_yolo_model("best.pt")
print("Loading BEiT model...")
beit_model = load_beit_model("epoch_12.pth")
print("Models loaded successfully!")


# --- 2. API ENDPOINT ---
@app.post("/analyze_outfit/")
async def analyze_outfit(image: UploadFile = File(...)):
    """
    This endpoint takes an image, runs it through the CV pipeline,
    and then gets fashion advice from the Gemini API.
    """
    image_bytes = await image.read()

    # Step A: Run YOLO to get cropped images
    cropped_clothes = run_yolo_on_image(yolo_model, image_bytes)

    # Step B: Run BEiT to classify the cropped images
    classified_items = {}
    for part, crop in cropped_clothes.items():
        classification = run_beit_on_image(beit_model, crop)
        classified_items[part] = classification
    
    # Step C: Call Gemini API for analysis and recommendations
    prompt = f"""
    Analyze these clothing items: {classified_items}.
    Based on fashion rules, generate 3 good combinations.
    Respond ONLY with a valid JSON object.
    """
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    response = gemini_model.generate_content(prompt)
    
    # Step D: Return the final result
    return {
        "identified_items": classified_items,
        "recommendations": response.text
    }


# --- 3. RUN THE SERVER ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
