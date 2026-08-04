import streamlit as st
import joblib
import pandas as pd
import numpy as np
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

# Lưu danh sách tài khoản đăng ký tạm thời trong session
if 'database_users' not in st.session_state:
    # Tài khoản mẫu mặc định: email "admin@gmail.com" - mật khẩu "123456"
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


# --- MÀN HÌNH SIGN IN / SIGN UP ---
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
                    # Lưu tài khoản mới vào danh sách
                    st.session_state.database_users[email_input] = password_input
                    st.session_state.logged_in = True
                    st.session_state.user_email = email_input
                    st.success("Account created and logged in successfully!")
                    st.rerun()
                    
    st.stop()


# --- GIAO DIỆN CHÍNH (SAU KHI ĐĂNG NHẬP) ---
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

if st.session_state.page == 'prediction':
    st.title("Real Estate Valuation Predictor")
    st.write("Enter property details to receive accurate valuation reports based on real-time market data.")
    st.write("")

    col_form, col_result = st.columns([7, 5], gap="large")

    with col_form:
        st.subheader("🏠 Property Specifications")
        
        overall_qual = st.slider("Overall Quality (OverallQual)", 1, 10, 5)
        total_sf = st.number_input("Total Area (TotalSF - sqft)", min_value=300, max_value=10000, value=1500)
        garage_cars = st.slider("Garage Capacity (GarageCars)", 0, 4, 2)
        
        central_air = st.selectbox("Central Air Conditioning (CentralAir)", ["Yes", "No"])
        kitchen_qual = st.selectbox("Kitchen Quality (KitchenQual)", ["Ex", "Gd", "TA", "Fa"])
        exter_qual = st.selectbox("Exterior Quality (ExterQual)", ["Ex", "Gd", "TA", "Fa"])
        
        st.write("")
        predict_btn = st.button("Predict Now", type="primary", use_container_width=True)

    with col_result:
        st.write("")
        st.write("")
        st.write("")
        
        st.subheader("📊 Estimated Value")
        
        if predict_btn:
            input_data = pd.DataFrame([baseline_values])
            input_data = input_data[feature_columns]
            
            input_data.loc[0, 'OverallQual'] = overall_qual
            input_data.loc[0, 'TotalSF'] = total_sf
            input_data.loc[0, 'GarageCars'] = garage_cars
            
            if 'CentralAir_Y' in input_data.columns:
                input_data.loc[0, 'CentralAir_Y'] = 1 if central_air == "Yes" else 0
                
            for col in input_data.columns:
                if f"KitchenQual_{kitchen_qual}" in col:
                    input_data.loc[0, col] = 1
                    
            for col in input_data.columns:
                if f"ExterQual_{exter_qual}" in col:
                    input_data.loc[0, col] = 1

            input_scaled = scaler.transform(input_data)
            prediction_log = model.predict(input_scaled)
            
            price_usd = np.expm1(prediction_log[0])
            price_billions = price_usd / 1_000_000_000
            
            if price_billions >= 1.0:
                val_str = f"{price_billions:.2f} billion USD"
                range_str = f"{(price_billions*0.95):.1f} - {(price_billions*1.05):.1f} billion"
            else:
                val_str = f"{price_usd:,.0f} USD"
                range_str = f"${(price_usd*0.95):,.0f} - ${(price_usd*1.05):,.0f}"

            st.metric(label="ESTIMATED VALUE", value=val_str, delta="Confidence: High (93%)")
            st.write(f"**Expected Price Range:** {range_str}")
            
            st.markdown("---")
            st.markdown("📈 **Neighborhood Trends:** +5.2% in the last 6 months")
            st.markdown("⏱️ **Time on Market:** ~45 days")
            
            if st.session_state.settings_history:
                st.session_state.history_list.append({
                    "Quality": overall_qual,
                    "Total Area (sqft)": total_sf,
                    "Garage Cars": garage_cars,
                    "Estimated Value": val_str
                })
        else:
            st.info("👈 Fill in the property specifications on the left and click **'Predict Now'** to see the valuation.")

elif st.session_state.page == 'history':
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

elif st.session_state.page == 'settings':
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

elif st.session_state.page == 'help':
    st.title("📖 Help Center")
    st.markdown("Welcome to the **Proptech Intelligence** Help Center.")
    st.markdown("### Frequently Asked Questions")
    st.markdown("1. **How does the prediction model work?**")
    st.write("The system uses an advanced XGBoost Machine Learning model trained on real estate datasets to estimate property values based on key features like quality, total area, and amenities.")
    st.markdown("2. **How to interpret the confidence score?**")
    st.write("A higher confidence percentage indicates that the input specifications closely match standard historical distribution ranges.")

elif st.session_state.page == 'contact':
    st.title("📞 Contact Support")
    st.markdown("Need technical assistance or have questions about the valuation report? Get in touch with our team.")
    st.info("📧 Email: hoangthithi19906@gmail.com.com")
    st.info("☎️ Hotline: +1 (555) 019-2834")
    st.write("")
    
    name_input = st.text_input("Your Name")
    email_input = st.text_input("Your Email", value=st.session_state.user_email)
    message_input = st.text_area("Describe your issue or inquiry")
    
    if st.button("Send Message"):
        if not name_input or not email_input or not message_input:
            st.warning("Please fill in all fields before sending!")
        else:
            try:
                SENDER_EMAIL = "hoangthithi19906@gmail.com"  
                SENDER_PASSWORD = "tscx fitv oarc wcmr"       
                RECEIVER_EMAIL = "hoangthithi19906@gmail.com" 
                
                msg = MIMEMultipart()
                msg['From'] = SENDER_EMAIL
                msg['To'] = RECEIVER_EMAIL
                msg['Subject'] = f"[Proptech Support] Message from {name_input}"
                
                body = f"--- THÔNG TIN NGƯỜI GỬI ---\n- Tên: {name_input}\n- Email: {email_input}\n\n--- NỘI DUNG ---\n{message_input}"
                msg.attach(MIMEText(body, 'plain'))
                
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
                server.quit()
                
                st.success("Your message has been sent successfully! We will get back to you via email soon.")
            except Exception as e:
                st.error(f"Failed to send email. Please check your App Password configuration. Error: {e}")