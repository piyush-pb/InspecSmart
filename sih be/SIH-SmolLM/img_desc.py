import streamlit as st
from dotenv import load_dotenv
import os
import torch
import streamlit as st
from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq
DEVICE = "cpu"
 
processor = AutoProcessor.from_pretrained("HuggingFaceTB/SmolVLM-Instruct")
model = AutoModelForVision2Seq.from_pretrained(
    "HuggingFaceTB/SmolVLM-Instruct",
    torch_dtype=torch.float32,   
    _attn_implementation="eager",   
).to(DEVICE)
def new_college():
    st.title("Image Descripter")
    st.write("Upload up to 3 images for description:")
    
    images = []
    for i in range(3):
        uploaded_image = st.file_uploader(f"Choose image {i + 1}", type=["jpg", "jpeg", "png"], key=f"image_{i}")
        if uploaded_image:
            img = Image.open(uploaded_image)
            images.append(img)
            st.image(img, caption=f"Image {i+1} Preview")
    
    if images:
        text = st.text_input("Enter your Instruction (if any)", value="Describe this Image in terms or quality and quantity.")
        submit_button = st.button("Submit")
    
        if submit_button: 
            messages = [
                {
                    "role": "user",
                    "content": [{"type": "image"} for _ in images] + [{"type": "text", "text": text}]
                }
            ]
             
            prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
            inputs = processor(text=prompt, images=images, return_tensors="pt")
            inputs = inputs.to(DEVICE)
    
            generated_ids = model.generate(**inputs, max_new_tokens=500)
            generated_texts = processor.batch_decode(
                generated_ids,
                skip_special_tokens=True,
            )
             
            assistant_text = generated_texts[0].split("Assistant:")[-1].strip()
            st.write("Assistant: ", assistant_text)
    