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

# Display the resized image
st.image(resized_logo, caption='Company Caption', use_column_width=True)

# Draw a horizontal line using HTML markup
st.markdown('<hr style="border: 2px solid orange; background-color: orange;">', unsafe_allow_html=True)

# Add title to my app with blue color
st.markdown("<h1 style='color: blue;'>Corporation Favorita - Sales System</h1>", unsafe_allow_html=True)

# Draw a horizontal line using HTML markup
st.markdown('<hr style="border: 2px solid orange; background-color: orange;">', unsafe_allow_html=True)

# Set the sidebar title
st.sidebar.title('Sales Prediction')

# Define the date range for prediction
new_start_date = pd.to_datetime('2023-01-01')
new_end_date = pd.to_datetime('2023-12-31')

# Create a date range
new_dates = pd.date_range(start=new_start_date, end=new_end_date, freq='D')

# Create a DataFrame with the new dates
new_data = pd.DataFrame({'Date': new_dates})

# Make predictions using the loaded SARIMAX model
predictions = sar_model.predict(start=new_data.index[0], end=new_data.index[-1])

# Round the predicted values to zero decimal places or as integers
new_data['Predicted Sales'] = predictions.round().astype(int)

# Display the predicted sales
st.title('Sales Prediction')

# Add a date selection sidebar widget
selected_date = st.sidebar.date_input('Select a Date', new_start_date, min_value=new_start_date, max_value=new_end_date)

# Filter the predicted data for the selected date
selected_date = pd.to_datetime(selected_date)
filtered_data = new_data[new_data['Date'].dt.date == selected_date.date()]

# Display the predicted sales for the selected date
st.subheader('Predicted Sales for {}'.format(selected_date.strftime('%Y-%m-%d')))
st.dataframe(filtered_data)

# Draw a horizontal line using HTML markup
st.markdown('<hr style="border: 2px solid orange; background-color: orange;">', unsafe_allow_html=True)

# Get user's selection for prediction type
prediction_type = st.sidebar.radio("Select Prediction Type", ('Daily', 'Weekly', 'Monthly'))

# Define the frequency based on the selected prediction type
if prediction_type == 'Daily':
    frequency = 'D'
elif prediction_type == 'Weekly':
    frequency = 'W'
elif prediction_type == 'Monthly':
    frequency = 'M'

# Create a date range
new_dates = pd.date_range(start=new_start_date, end=new_end_date, freq=frequency)

# Create a DataFrame with the new dates
new_data = pd.DataFrame({'Date': new_dates})

# Make predictions using the loaded SARIMAX model
predictions = sar_model.predict(start=new_data.index[0], end=new_data.index[-1])

# Round the predicted values to zero decimal places or as integers
new_data['Predicted Sales'] = predictions.round().astype(int)

# Display the predicted sales
st.subheader(f'Predicted Sales for {prediction_type} Sales')
st.dataframe(new_data)

# Display a plot of the predicted sales
st.subheader(f'Plot of Predicted {prediction_type} Sales')
st.line_chart(new_data.set_index('Date')['Predicted Sales'])