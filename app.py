import streamlit as st
from PIL import Image
# --- NEW IMPORTS ---
# Import the wrapper functions from your new files
from yolo_model import run_yolo_detection
from beit_model import run_beit_classification

# ... (keep all your other functions like remove_background, find_dominant_color, etc.) ...


# --- MAIN APP INTERFACE ---
st.title("Project Stylica 🚀")
st.write(f"Welcome, {st.session_state.username}!")

st.header("1. Add Clothes via Photo")
# Changed to a single file uploader for the new workflow
uploaded_file = st.file_uploader(
    "Upload a picture of your closet or an outfit...", 
    type=["jpg", "png", "jpeg"]
)

if uploaded_file is not None:
    st.image(uploaded_file, caption='Uploaded Image.', use_container_width=True)
    
    if st.button('Analyze Photo'):
        # --- NEW TWO-STAGE AI PIPELINE ---
        with st.spinner('Detecting clothing items...'):
            # Step 1: Run YOLO to find and crop clothes
            cropped_images = run_yolo_detection(uploaded_file)
        
        if not cropped_images:
            st.warning("No clothing items were detected in the image.")
        else:
            st.success(f"Detected {len(cropped_images)} items! Now classifying each one...")
            
            progress_bar = st.progress(0, text="Classifying items...")
            
            # Step 2: Loop through cropped images and run BEiT on each one
            for i, cropped_image in enumerate(cropped_images):
                progress_bar.progress((i + 1) / len(cropped_images), text=f"Classifying item {i+1}...")
                
                # Get the clothing type from your BEiT model
                item_type = run_beit_classification(cropped_image)
                
                # --- (Your existing analysis logic) ---
                item_category = label_to_category.get(item_type.lower().replace('-', '').replace(' ', ''), 'unknown')
                image_no_bg = remove_background(cropped_image)
                item_color_rgb = find_dominant_color(image_no_bg)
                
                final_item = {
                    'category': item_category,
                    'type': item_type,
                    'color': item_color_rgb
                }
                st.session_state.wardrobe.append(final_item)

            progress_bar.empty()
            st.success("Analysis Complete! All detected items added to your wardrobe.")
            st.rerun()

# ... (The rest of your code for recommendations and wardrobe display remains the same) ...