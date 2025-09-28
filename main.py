# main.py (Corrected Logic)

from fastapi import FastAPI, UploadFile, File
import uvicorn
import os
import google.generativeai as genai

# Your model scripts with the corrected code from the previous step
from yolo_model import run_yolo_detection # This should return a LIST of cropped images now
from beit_model import run_beit_classification 

# --- 1. INITIALIZATION ---
app = FastAPI(title="Stylia AI Engine")
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
print("Models are being loaded by their respective scripts...")

# --- 2. API ENDPOINT ---
@app.post("/analyze_outfit/")
async def analyze_outfit(image: UploadFile = File(...)):
    """
    This endpoint correctly uses YOLO for cropping and BEiT for classification.
    """
    image_bytes = await image.read()

    # Step A: Run YOLO to get a LIST of cropped PIL images
    # The original yolo code you sent works perfectly for this.
    list_of_cropped_images = run_yolo_detection(image_bytes)

    if not list_of_cropped_images:
        return {"error": "No clothing items were detected in the image."}

    # Step B: Loop through each crop and classify it with BEiT
    identified_items = []
    for crop in list_of_cropped_images:
        # Get the specific class name (e.g., "Men__Jeans", "Women__Tops")
        specific_label = run_beit_classification(crop)
        identified_items.append(specific_label)
    
    # Step C: Call Gemini API with the list of identified items
    prompt = f"""
    A user is wearing the following items: {identified_items}.
    Analyze this outfit. Based on fashion rules, generate 3 good combinations or style suggestions.
    Respond ONLY with a valid JSON object.
    """
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    response = gemini_model.generate_content(prompt)
    
    # Step D: Return the final result
    return {
        "identified_items": identified_items,
        "recommendations": response.text
    }

# --- 3. RUN THE SERVER ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
