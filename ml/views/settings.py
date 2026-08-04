import streamlit as st

def render():
    st.title("⚙️ System Settings")
    st.write("Configure machine learning model parameters and application preferences:")
    
    temp_stream = st.checkbox("Enable Real-time Market Data Stream", value=st.session_state.settings_stream)
    temp_history = st.checkbox("Automatically Save Search History", value=st.session_state.settings_history)
    temp_model_version = st.text_input("Active Model Version", value=st.session_state.settings_model_version)
    
    if st.button("Save Changes"):
        st.session_state.settings_stream = temp_stream
        st.session_state.settings_history = temp_history
        st.session_state.settings_model_version = temp_model_version
        st.success("Settings saved successfully!")