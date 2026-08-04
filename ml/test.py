import streamlit as st
import joblib
import pandas as pd
import os

# Import các trang từ thư mục views nằm trong ml/
from views import prediction, history, settings, help_center, contact

st.set_page_config(
    page_title="Proptech Intelligence - Real Estate Valuation",
    page_icon="🏠",
    layout="wide"
)

st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #00C896;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
    }
    div.stButton > button:first-child:hover {
        background-color: #00b084;
        color: white;
    }
    .stSlider, .stNumberInput, .stSelectbox {
        margin-bottom: -10px !important;
    }
    </style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_assets():
    model = joblib.load(os.path.join(BASE_DIR, 'model', 'house_price_model.pkl'))
    scaler = joblib.load(os.path.join(BASE_DIR, 'model', 'scaler.pkl'))
    feature_columns = joblib.load(os.path.join(BASE_DIR, 'model', 'feature_columns.pkl'))
    
    baseline_path = os.path.join(BASE_DIR, 'model', 'baseline_values.pkl')
    if os.path.exists(baseline_path):
        baseline_values = joblib.load(baseline_path)
    else:
        baseline_values = pd.Series(0, index=feature_columns)
        
    return model, scaler, feature_columns, baseline_values

model, scaler, feature_columns, baseline_values = load_assets()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'user_email' not in st.session_state:
    st.session_state.user_email = ""

if 'database_users' not in st.session_state:
    st.session_state.database_users = {"admin@gmail.com": "123456"}

if 'page' not in st.session_state:
    st.session_state.page = 'prediction'

if 'history_list' not in st.session_state:
    st.session_state.history_list = []

if 'settings_stream' not in st.session_state:
    st.session_state.settings_stream = True

if 'settings_history' not in st.session_state:
    st.session_state.settings_history = True

if 'settings_model_version' not in st.session_state:
    st.session_state.settings_model_version = "XGBoost_Ames_v1.2"

# MÀN HÌNH SIGN IN / SIGN UP
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_space1, col_auth, col_space2 = st.columns([2, 3, 2])
    
    with col_auth:
        st.markdown("## 🏢 Proptech Intelligence")
        st.caption("Sign in to your account to continue precision valuation.")
        st.write("")
        
        auth_mode = st.radio("Choose action", ["Sign In", "Register"], horizontal=True, label_visibility="collapsed")
        
        email_input = st.text_input("Email Address")
        password_input = st.text_input("Password", type="password")
        
        st.write("")
        if auth_mode == "Sign In":
            if st.button("Sign In", use_container_width=True, type="primary"):
                if not email_input or not password_input:
                    st.warning("Please enter both email and password.")
                elif email_input in st.session_state.database_users and st.session_state.database_users[email_input] == password_input:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email_input
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Incorrect email or password. Please try again.")
        else:
            if st.button("Create Account", use_container_width=True, type="primary"):
                if not email_input or not password_input:
                    st.warning("Please fill in all fields to register.")
                elif email_input in st.session_state.database_users:
                    st.error("This email is already registered. Please sign in instead.")
                else:
                    st.session_state.database_users[email_input] = password_input
                    st.session_state.logged_in = True
                    st.session_state.user_email = email_input
                    st.success("Account created and logged in successfully!")
                    st.rerun()
                    
    st.stop()

# GIAO DIỆN CHÍNH (SAU KHI ĐĂNG NHẬP)
col_top1, col_top2 = st.columns([10, 2])
with col_top1:
    st.caption(f"Connected as: **{st.session_state.user_email}**")
with col_top2:
    if st.button("Sign Out"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.rerun()

with st.sidebar:
    st.markdown("### 🏢 Proptech Intelligence")
    st.caption("Precision Valuation")
    st.divider()
    
    if st.button("➕ New Analysis", use_container_width=True):
        st.session_state.page = 'prediction'
    if st.button("📊 New Prediction", use_container_width=True, type="primary"):
        st.session_state.page = 'prediction'
    if st.button("🕒 History", use_container_width=True):
        st.session_state.page = 'history'
    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.page = 'settings'
    
    st.divider()
    st.markdown("#### 💡 Support")
    if st.button("📖 Help Center", use_container_width=True):
        st.session_state.page = 'help'
    if st.button("📞 Contact Support", use_container_width=True):
        st.session_state.page = 'contact'

# ĐIỀU HƯỚNG HIỂN THỊ CÁC TRANG
if st.session_state.page == 'prediction':
    prediction.render(model, scaler, feature_columns, baseline_values)
elif st.session_state.page == 'history':
    history.render()
elif st.session_state.page == 'settings':
    settings.render()
elif st.session_state.page == 'help':
    help_center.render()
elif st.session_state.page == 'contact':
    contact.render()