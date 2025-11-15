import streamlit as st
import pandas as pd
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import importlib.util
import streamlit as st

if importlib.util.find_spec("openpyxl") is None:
    st.error("❌ openpyxl is NOT installed in this environment")
else:
    st.success("✅ openpyxl is installed and ready")
    
# ---- Streamlit UI ----
st.title("Hariom Industries Bulk Email Sender")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv","xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        data = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        data = pd.read_excel(uploaded_file, engine="openpyxl")


    # ---- Gmail Credentials ----
    sender_email = st.text_input("Sender Email")
    password = st.text_input("App Password", type="password")

    # ---- Batching Settings ----
    BATCH_SIZE = st.number_input("Batch size", min_value=10, max_value=100, value=30)
    DELAY = st.number_input("Delay between batches (seconds)", min_value=60, max_value=600, value=180)

    if st.button("Start Sending Emails"):
        smtp_server = "smtp.gmail.com"
        port = 587
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)

        recipients = data.to_dict("records")
        sent_count = 0
        log_entries = []

        def generate_email(unit_name):
            return f"""
Respected Sir/Madam,

I am Mayur Thakkar from Hariom Industries, Harij, Dist. Patan, Gujarat – 384240.
We specialize in supplying cotton bales and cotton seed with strict quality standards,
serving both domestic and international markets.

Our cotton bales are processed and packed to ensure consistency in fiber quality for spinning mills,
while our cotton seed is clean and graded for oil extraction and allied uses.
We take pride in maintaining transparent processes, reliable supply, and building long-term partnerships
through trust, fair pricing, and timely delivery.

If you would like to connect with us, please reach out at the email address below
with your requirement details. We will be glad to share specifications, pricing,
and supply terms tailored to your needs.

Sincerely,
Hariom Industries
Harij, Dist. Patan, Gujarat – 384240
📩 Hariomindustries5559@gmail.com

------------------------------------------------------------
Important Note:
This email is being sent to you from available mail IDs across the Internet
for business inquiry purposes. If you would like to UNSUBSCRIBE,
please reply to this mail with the word UNSUBSCRIBE.
------------------------------------------------------------
"""

        for i, rec in enumerate(recipients, start=1):
            unit_name = rec.get("Unit Name", "your esteemed organization")
            email = rec.get("Email")

            if pd.isna(email):
                continue

            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = email
            msg["Subject"] = "Introduction – Hariom Industries"
            msg.attach(MIMEText(generate_email(unit_name), "plain"))

            try:
                server.sendmail(sender_email, email, msg.as_string())
                sent_count += 1
                st.success(f"✅ Sent to {unit_name} ({email})")
                status = "Sent"
            except Exception as e:
                st.error(f"❌ Failed to send to {unit_name} ({email}): {e}")
                status = f"Failed: {e}"

            log_entries.append({
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Unit Name": unit_name,
                "Email": email,
                "Status": status
            })

            if i % BATCH_SIZE == 0:
                st.warning(f"⏸ Pausing for {DELAY} seconds after {BATCH_SIZE} emails...")
                time.sleep(DELAY)

        server.quit()
        st.info(f"🎉 Finished sending {sent_count} emails.")

        # ---- Save Log ----
        log_df = pd.DataFrame(log_entries)
        log_df.to_csv("sent_log.csv", index=False)
        st.success("📝 Log saved to sent_log.csv")
