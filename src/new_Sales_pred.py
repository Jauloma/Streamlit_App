import streamlit as st
import pandas as pd
import pickle
from PIL import Image

# Load the pre-trained model
with open('sarimax_model.pickle', 'rb') as f:
    sar_model = pickle.load(f)

# Add Company Logo
comp_logo = Image.open('Corp_logo2.png')
# Resize the image
resized_logo = comp_logo.resize((500, 500))  # Adjust the size of image

