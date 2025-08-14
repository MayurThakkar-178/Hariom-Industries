import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Page settings
st.set_page_config(page_title="Office Space HTML Email Sender", layout="centered")
st.title("🏢 Fully Furnished Office Space – HTML Email Broadcaster")
st.write("Upload an Excel file of contacts and send a professionally styled HTML flyer.")

# Upload Excel contacts
uploaded_file = st.file_uploader("📂 Upload Excel File (.xlsx)", type=["xlsx"])

if uploaded_file:
    # Read the contact list
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip().str.title()

    st.subheader("📋 Contacts Preview")
    st.dataframe(df)

    # Gmail credentials
    st.subheader("✉️ Gmail Sender Details")
    sender_email = st.text_input("Sender Gmail", placeholder="example@gmail.com")
    app_password = st.text_input("App Password (Gmail App Password)", type="password")

    # Email subject
    subject = "📢 Fully Furnished Office Space for Rent – CG Road, Ahmedabad"

    # HTML Email Body Template
    office_html_message = """
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <p>Dear {name},</p>
        
        <h2 style="color:#d35400;">📢 Fully Furnished Office Space for Rent – CG Road, Ahmedabad</h2>
        
        <p><b>📍 Location:</b> Kalapurnam Complex, Near Municipal Market, CG Road, Navrangpura, Ahmedabad</p>
        <p><b>📌 Google Map:</b> <a href="https://maps.app.goo.gl/zfzrn4cP2dGbPpk46?g_st=ipc" style="color:#2980b9;">View Location</a></p>
        <p><b>📐 Area:</b> 2632 sq.ft</p>
        <p><b>💰 Rent:</b> ₹48/sq.ft (Approx. ₹1,26,336 per month)</p>
        
        <h3 style="color:#27ae60;">🏢 Office Features:</h3>
        <ul>
            <li>Boss cabin</li>
            <li>Manager cabin</li>
            <li>Conference room</li>
            <li>Reception area</li>
            <li>50–70 workstation capacity</li>
            <li>Pantry</li>
            <li>8–10 Air Conditioning units</li>
            <li>Sofas & Chairs</li>
            <li>Separate male & female washrooms</li>
        </ul>

        <p>✅ Ready-to-move-in<br>
           ✅ Prime Commercial Location<br>
           ✅ Ideal for Corporate, IT, or Service-based Companies</p>

        <h3 style="color:#c0392b;">📞 Contact:</h3>
        <p>
            <b>Prakash Thakkar</b> – +91 98790 92111<br>
            <b>Manoj Thakkar</b> – +91 98253 20376
        </p>

        <p style="margin-top:30px;">Best regards,<br>Hariom Group</p>
    </body>
    </html>
    """

    # Send Emails Button
    if st.button("📬 Send HTML Emails"):
        if not sender_email or not app_password:
            st.error("Please provide your Gmail and App Password.")
        else:
            sent_count = 0
            for _, row in df.iterrows():
                name = row.get("Name", "")
                recipient = row.get("Email", "")

                if not recipient:
                    continue  # skip empty emails

                # Personalize and prepare email
                final_html = office_html_message.format(name=name)
                msg = MIMEMultipart("alternative")
                msg['From'] = sender_email
                msg['To'] = recipient
                msg['Subject'] = subject
                msg.attach(MIMEText(final_html, "html"))

                try:
                    with smtplib.SMTP("smtp.gmail.com", 587) as server:
                        server.starttls()
                        server.login(sender_email, app_password)
                        server.sendmail(sender_email, recipient, msg.as_string())
                        sent_count += 1
                        st.success(f"✅ HTML Email Sent to {name} <{recipient}>")
                        time.sleep(1)  # delay to avoid Gmail throttling
                except Exception as e:
                    st.error(f"❌ Failed to send to {recipient}: {e}")
                    time.sleep(1)

            st.info(f"📧 Total HTML Emails Sent: {sent_count}")
