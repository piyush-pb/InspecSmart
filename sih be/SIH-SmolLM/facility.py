import streamlit as st
from ultralytics import YOLO
from PIL import Image
import os
import pandas as pd

model = YOLO("best.pt")

class_names = [
    'auditoriums', 'bench', 'canteen', 'chairs', 'classroom', 'library', 
    'lift', 'path', 'stairs', 'system', 'toilet', 'urinals', 
    'washbasin', 'washroom'
]

def process_images(uploaded_files, confidence):
    results_data = []

    st.subheader("Processed Images and Predictions")
    for uploaded_file in uploaded_files: 
        image = Image.open(uploaded_file)
         
        st.image(image, caption=f"Raw Image: {uploaded_file.name}")
        
        temp_image_path = f"{uploaded_file.name}"
        image.save(temp_image_path)
 
        results = model(temp_image_path, save=True, conf=confidence)
         
        prediction_dirs = [d for d in os.listdir("runs\\detect") if d.startswith("predict")]
         
        prediction_dirs.sort(reverse=True)
        latest_prediction_dir = os.path.join("runs\\detect", prediction_dirs[0])
 
        predicted_image_path = os.path.join(latest_prediction_dir, uploaded_file.name)
         
        st.write(f"Predicted image full path: {predicted_image_path}")
 
        for result in results:  
            for box in result.boxes:
                class_index = int(box.cls[0])   
                class_name = class_names[class_index]   
                confidence_score = float(box.conf[0]) 
                results_data.append({
                    "Image": uploaded_file.name,
                    "Class": class_name,
                    "Confidence": confidence_score
                })
        os.remove(temp_image_path)

    return results_data

def summarize_results(results_data):
    if results_data:
        df = pd.DataFrame(results_data)
        summary = df.groupby("Class").size().reset_index(name="Count")
        st.subheader("Summary Table")
        summary = summary.style.hide(axis='index')
        
        st.table(summary)  
    else:
        st.write("No predictions were made.")



def facility():
    st.title("Facility Inspection")
     
    uploaded_files = st.file_uploader(
        "Upload Images for Prediction", type=["jpg", "jpeg", "png"], accept_multiple_files=True
    )
 
    confidence = st.slider(
        "Confidence Threshold", min_value=0.0, max_value=1.0, value=0.1, step=0.01
    )
 
    if uploaded_files:
        results_data = process_images(uploaded_files, confidence)
        summarize_results(results_data)