import streamlit as st

def render():
    st.title("📖 Help Center")
    st.markdown("Welcome to the **Proptech Intelligence** Help Center.")
    st.markdown("### Frequently Asked Questions")
    st.markdown("1. **How does the prediction model work?**")
    st.write("The system uses an advanced XGBoost Machine Learning model trained on real estate datasets to estimate property values based on key features like quality, total area, and amenities.")
    st.markdown("2. **How to interpret the confidence score?**")
    st.write("A higher confidence percentage indicates that the input specifications closely match standard historical distribution ranges.")