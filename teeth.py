import streamlit as st
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

st.title("🦷 Open Your Mouth ")

@st.cache_resource
def load_my_model():
    return load_model("teeth_classifier.h5")

model = load_my_model()

option = st.radio(
    "Choose input method:",
    ("📷 Camera", "📁 Upload Image")
)

img = None
labels=['CaS', 'CoS', 'Gum', 'MC', 'OC', 'OLP', 'OT']

if option == "📷 Camera":
    camera = st.camera_input("Take a photo")
    if camera:
        img = Image.open(camera)
elif option == "📁 Upload Image":
    uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded:
        img = Image.open(uploaded).convert("RGB")

if img:
    img_array = np.array(img)
    st.image(img_array, caption="Input Image", use_column_width=True)

    frame_resized = cv2.resize(img_array, (224, 224))
    frame_norm = frame_resized / 255.0
    frame_norm = np.expand_dims(frame_norm, axis=0)  
    
    prediction = model.predict(frame_norm)
    prediction=np.argmax(prediction)
    st.write("Your disease :", labels[prediction])
