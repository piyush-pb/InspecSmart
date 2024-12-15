import streamlit as st
from PIL import Image
import os

def home_operation():
    st.title("Predicted Facilities")

    base_dir = r"C:\SIH-SmolLM\runs\detect"

    if not os.path.exists(base_dir):
        st.error(f"Base directory not found: {base_dir}")
        return

    predict_dirs = [
        os.path.join(base_dir, d) for d in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, d)) and d.startswith("predict") and (d == "predict" or d[7:].isdigit())
    ]

    predict_dirs.sort(key=lambda x: int(x.split('predict')[-1]) if x.split('predict')[-1].isdigit() else -1)

    if not predict_dirs:
        st.warning("No prediction directories found.")
        return

    for predict_dir in predict_dirs:
        st.subheader(f"Images in: {predict_dir}")
        for file_name in os.listdir(predict_dir):
            file_path = os.path.join(predict_dir, file_name)
            if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
                try:
                    image = Image.open(file_path)
                    st.image(image, caption=f"Image: {file_name}")
                except Exception as e:
                    st.error(f"Error loading image {file_name}: {e}")