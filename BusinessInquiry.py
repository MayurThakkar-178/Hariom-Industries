import streamlit as st
import pandas as pd
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import importlib.util

# ----------------------------
#        CUSTOM STYLING
# ----------------------------
st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
    }
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #1a237e;
        margin-bottom: -20px;
    }
    .subtitle {
        text-align: center;
        color: #424242;
        font-size: 16px;
        margin-bottom: 20px;
    }
    .card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    .stButton>button {
        background-color: #1e88e5;
        color: white;
        width: 100%;
        border-radius: 10px;
        height: 50px;
        font-size: 18px;
    }
    .stButton>button:hover {
        background-color: #1565c0;
    }
    .email-preview {
        background: #e3f2fd;
        padding: 15px;
        border-radius: 10px;
        font-size: 14px;
        color: #0d47a1;
        border-left: 5px solid #1565c0;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
#        BANNER IMAGE
# ----------------------------
st.image("banner.png", use_column_width=True)

# ----------------------------
#        TITLE SECTION
# ----------------------------
st.markdown('<div class="title">Hariom Industries</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Bulk Email Sender – Cotton Bales & Seeds</div>', unsafe_allow_html=True)

# ----------------------------
# Check openpyxl
# ----------------------------
if importlib.util.find_spec("openpyxl") is None:
    st.error("❌ openpyxl is NOT installed in this environment")
else:
    st.success("✅ openpyxl is installed and ready")

# ----------------------------
#        FILE UPLOAD
# ----------------------------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("📤 Upload CSV or XLSX with Unit Name & Email", type=["csv","xlsx"])
    st.markdown('</div>', unsafe_allow_html=True)


if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file, engine="openpyxl")

    # ----------------------------
    #  GMAIL LOGIN SECTION
    # ----------------------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📧 Email Credentials")
    sender_email = st.text_input("Sender Email")
    password = st.text_input("App Password", type="password")
    st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------
    #  FORMATTING SETTINGS
    # ----------------------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("⚙️ Email Sending Settings")
    BATCH_SIZE = st.number_input("Batch size", min_value=10, max_value=200, value=30)
    DELAY = st.number_input("Delay between batches (seconds)", min_value=30, max_value=600, value=180)
    st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------
    # EMAIL PREVIEW SECTION
    # ----------------------------
    def generate_email(unit_name):
        return f"""
Respected Sir/Madam,

Greetings from Hariom Industries, Harij, Dist. Patan, Gujarat.

We are a leading supplier of high-quality Cotton Bales (Shankar-6 variety) and Cotton Seeds, serving spinning mills and oil units across India. With a strong operational setup and a commitment to consistent quality, we aim to build long-term supply partnerships with reputed mills like yours.

Our manufacturing and ginning processes follow strict quality checks to ensure:
• Uniform fiber length  
• Low trash content  
• Optimal moisture levels  
• Highly stable and contamination-free bales  
• Reliable packaging suitable for bulk transport  

We supply:
• *Shankar-6 Cotton Bales*  
• *Cotton Seeds (for oil extraction)*  
• *Customized pressing & packing based on client needs*  

Hariom Industries ensures:
• Consistent quality in every lot  
• Transparent pricing  
• Fast and reliable dispatch from Gujarat  
• Long-term supply capability  
• Customized bale specifications on request  

If you would like to receive quotations, technical specifications, dispatch schedules or sample details, please feel free to share your requirement (quantity, variety, and delivery location).  
We will be pleased to provide the best rates tailored to your mill’s needs.

Looking forward to the opportunity to associate with your esteemed organization.

Best Regards,  
**Hariom Industries**  
Harij, Dist. Patan, Gujarat – 384240  
📩 Hariomindustries5559@gmail.com  
📞 (Add your phone number here)

------------------------------------------------------------
This email is sent only for business inquiry and information purposes.  
If you wish to UNSUBSCRIBE, please reply with the word “UNSUBSCRIBE”.
------------------------------------------------------------
"""

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📄 Email Preview")
    st.markdown(f"<div class='email-preview'>{generate_email('Unit Name Example')}</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------
    # START SENDING EMAILS
    # ----------------------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if st.button("🚀 Start Sending Emails"):
        smtp_server = "smtp.gmail.com"
        port = 587
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)

        recipients = data.to_dict("records")
        sent_count = 0
        log_entries = []

        progress_bar = st.progress(0)

        for i, rec in enumerate(recipients, start=1):
            unit_name = rec.get("Unit Name", "valued organization")
            email = rec.get("Email")

            if pd.isna(email) or "@" not in email:
                continue

            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = email
            msg["Subject"] = "Introduction – Hariom Industries"
            msg.attach(MIMEText(generate_email(unit_name), "plain"))

            try:
                server.sendmail(sender_email, email, msg.as_string())
                sent_count += 1
                st.success(f"📨 Sent to {unit_name} ({email})")
                status = "Sent"
            except Exception as e:
                st.error(f"❌ Failed to {email}: {e}")
                status = "Failed"

            log_entries.append({
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Unit Name": unit_name,
                "Email": email,
                "Status": status
            })

            progress_bar.progress(i / len(recipients))

            if i % BATCH_SIZE == 0:
                st.warning(f"⏸ Waiting {DELAY}s before next batch...")
                time.sleep(DELAY)

        server.quit()

        log_df = pd.DataFrame(log_entries)
        log_df.to_csv("sent_log.csv", index=False)
        st.success(f"🎉 Completed! {sent_count} emails sent successfully.")
        st.info("📝 Log saved as sent_log.csv")

    st.markdown('</div>', unsafe_allow_html=True)
