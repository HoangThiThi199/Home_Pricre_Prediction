import streamlit as st
import joblib
import pandas as pd
import numpy as np

model = joblib.load('model/house_price_model.pkl')
scaler = joblib.load('model/scaler.pkl')
feature_columns = joblib.load('model/feature_columns.pkl')

st.title("House price prediction")

# Form nhập liệu 
overall_qual = st.slider("Overall_qual(1-10)", 1, 10, 5)
gr_liv_area = st.number_input("gr_liv_area (sqft)", min_value=300, max_value=6000, value=1500)
garage_cars = st.slider("garage_cars", 0, 4, 2)
total_bsmt_sf = st.number_input("Diện tích tầng hầm (sqft)", min_value=0, max_value=3000, value=800)
year_built = st.number_input("year_built", min_value=1870, max_value=2026, value=2000)

if st.button("Predict your house"):
    input_data = pd.DataFrame(np.zeros((1, len(feature_columns))), columns=feature_columns)

    input_data['OverallQual'] = overall_qual
    input_data['GrLivArea'] = gr_liv_area
    input_data['GarageCars'] = garage_cars
    input_data['TotalBsmtSF'] = total_bsmt_sf
    input_data['YearBuilt'] = year_built

    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)

    st.success(f"Predicted Price: {prediction[0]:,.0f} USD")