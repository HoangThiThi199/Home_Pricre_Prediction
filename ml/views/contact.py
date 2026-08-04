import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def render():
    st.title("📞 Contact Support")
    st.markdown("Need technical assistance or have questions about the valuation report? Get in touch with our team.")
    st.info("📧 Email: hoangthithi19906@gmail.com")
    st.info("☎️ Hotline: 12345678")
    st.write("")
    
    name_input = st.text_input("Your Name")
    email_input = st.text_input("Your Email", value=st.session_state.user_email)
    message_input = st.text_area("Describe your issue or inquiry")
    
    if st.button("Send Message"):
        if not name_input or not email_input or not message_input:
            st.warning("Please fill in all fields before sending!")
        else:
            try:
                SENDER_EMAIL = st.secrets["SENDER_EMAIL"]
                SENDER_PASSWORD = st.secrets["SENDER_PASSWORD"]
                RECEIVER_EMAIL = st.secrets["SENDER_EMAIL"]
                
                # 1. GỬI THƯ BÁO VỀ CHO ADMIN
                msg_to_admin = MIMEMultipart()
                msg_to_admin['From'] = SENDER_EMAIL
                msg_to_admin['To'] = RECEIVER_EMAIL
                msg_to_admin['Subject'] = f"[Proptech Support] Message from {name_input}"
                
                body_admin = f"--- THÔNG TIN NGƯỜI GỬI ---\n- Tên: {name_input}\n- Email: {email_input}\n\n--- NỘI DUNG ---\n{message_input}"
                msg_to_admin.attach(MIMEText(body_admin, 'plain', 'utf-8'))
                
                # 2. GỬI THƯ TỰ ĐỘNG XÁC NHẬN (AUTO-REPLY) CHO KHÁCH HÀNG 
                msg_to_user = MIMEMultipart()
                msg_to_user['From'] = SENDER_EMAIL
                msg_to_user['To'] = email_input 
                msg_to_user['Subject'] = "[Proptech Intelligence] We have received your support request!"
                
                body_user = f"Hi {name_input},\n\nThank you for contacting Proptech Intelligence Support! We have received your message and will review it shortly.\n\nBest regards,\nProptech Support Team"
                msg_to_user.attach(MIMEText(body_user, 'plain', 'utf-8'))
                
                # 3. KẾT NỐI SMTP VÀ GỬI CẢ HAI THƯ 
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg_to_admin.as_string())
                server.sendmail(SENDER_EMAIL, email_input, msg_to_user.as_string())
                
                server.quit()
                
                st.success("Your message has been sent successfully! A confirmation email has also been sent to your inbox.")
            except Exception as e:
                st.error(f"Failed to send email. Please check your App Password configuration. Error: {e}")