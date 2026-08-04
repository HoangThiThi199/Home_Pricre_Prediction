import streamlit as st
import pandas as pd

def render():
    st.title("🕒 Prediction History")
    st.write("List of recent property valuations in your current session:")
    
    if st.session_state.settings_history:
        if len(st.session_state.history_list) > 0:
            df_history = pd.DataFrame(st.session_state.history_list)
            st.dataframe(df_history, use_container_width=True)
        else:
            st.info("No valuation history found. Go back to **New Prediction** and run a prediction first!")
    else:
        st.warning("History saving is currently disabled in **Settings**.")