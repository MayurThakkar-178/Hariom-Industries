import streamlit as st
import pandas as pd
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import importlib.util

# ----------------------------
#        CUSTOM CSS STYLING
# ----------------------------
st.markdown("""
<style>
    .main { background-color: #f5f7fa; }
    .title {
        text-align: center; font-size: 36px; font-weight: bold;
        color: #1a237e; margin-bottom: -10px;
    }
    .subtitle {
        text-align: center; font-size: 16px; color: #424242; margin-bottom: 25px;
    }
    .card {
        background: white; padding: 20px; border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1); margin-bottom: 25px;
    }
    .stButton>button {
        background-color: #1e88e5; color: white; width: 100%; border-radius: 10px;
        height: 50px; font-size: 18px;
    }
    .stButton>button:hover { background-color: #1565c0; }
    .email-preview {
        background: #e3f2fd; padding: 15px; border-radius: 10px;
        font-size: 14px; color: #0d47a1; border-left: 5px solid #1565c0;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
#        APP BANNER
# ----------------------------
st.image("Hariom.png", use_column_width=True)

# ----------------------------
#        TITLE
# ----------------------------
st.markdown('<div class="title">Hariom Industries</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Bulk Email Sender – Cotton Bales & Cotton Seeds</div>',
            unsafe_allow_html=True)

# ----------------------------
#  OPENPYXL CHECK
# ----------------------------
if importlib.util.find_spec("openpyxl") is None:
    st.error("❌ openpyxl is not installed")
else:
    st.success("✅ openpyxl ready")

# ----------------------------
#  FILE UPLOADER
# ----------------------------

uploaded_file = st.file_uploader("📤 Upload CSV or XLSX with Unit Name & Email", type=["csv", "xlsx"])

# ==============================================================
#       INLINE BANNER EMAIL BUILDER (CID EMBED)
# ==============================================================
def build_email(unit_name, sender_email, receiver_email):

    msg = MIMEMultipart("related")
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Introduction – Hariom Industries"

    # ---------- HTML BODY ----------
    html = f"""
    <html>
    <body>

    <div style="text-align:center;">
        <img src="cid:banner_image" style="width:100%; max-width:750px; border-radius:10px;">
    </div>

    <br>

    <p>Respected Sir/Madam,</p>

    <p>
    Greetings from <b>Hariom Industries, Harij, Dist. Patan, Gujarat.</b><br>
    We specialize in supplying high-quality <b>Shankar-6 Cotton Bales</b> and 
    <b>Cotton Seed</b> for spinning mills and oil units across India.
    </p>

    <p>
    Our strengths include:
    <ul>
        <li>Uniform contamination-free bales</li>
        <li>Low trash and stable fibre length</li>
        <li>Moisture-controlled packing</li>
        <li>Timely dispatches from Gujarat</li>
        <li>Transparent pricing</li>
    </ul>
    </p>

    <p>
    To receive quotations, bale specs or dispatch details, kindly share your 
    requirement (quantity + delivery location). We will respond with a tailored offer.
    </p>

    <p>We look forward to serving your esteemed mill.</p>

    <br>

    <b>Regards,<br>
    Hariom Industries</b><br>
    Harij, Dist. Patan, Gujarat – 384240<br>
    📩 Hariomindustries5559@gmail.com<br>

    <hr>
    <p style="font-size:12px; color:#555;">
    This email is for business inquiries only.  
    Reply with <b>UNSUBSCRIBE</b> to stop further emails.
    </p>

    </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    # ---------- INLINE BANNER ATTACHMENT ----------
    with open("Hariom.png", "rb") as f:
        img = MIMEImage(f.read())
        img.add_header("Content-ID", "<banner_image>")
        img.add_header("Content-Disposition", "inline", filename="banner.png")
        msg.attach(img)

    return msg


# ==============================================================
#               PROCESS EMAIL SENDING
# ==============================================================

if uploaded_file is not None:

    # Read file
    if uploaded_file.name.endswith(".csv"):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file, engine="openpyxl")

    # ----------------------------
    #  EMAIL LOGIN
    # ----------------------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📧 Email Credentials")
    sender_email = st.text_input("Your Gmail")
    password = st.text_input("App Password", type="password")
    st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------
    #  SETTINGS
    # ----------------------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("⚙️ Settings")
    BATCH_SIZE = st.number_input("Batch size", 10, 300, 50)
    DELAY = st.number_input("Delay between batches (seconds)", 30, 600, 180)
    st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------
    #  EMAIL PREVIEW
    # ----------------------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📄 Email Preview")
    st.markdown("""
    <div class='email-preview'>
        (Preview not showing inline image, but receivers will see full banner)
        <br><br>
        Respected Sir/Madam,<br>
        Greetings from Hariom Industries...
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ----------------------------
    #  SEND BUTTON
    # ----------------------------
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if st.button("🚀 Start Sending Emails"):
        timer_placeholder = st.empty()
        smtp_server = "smtp.gmail.com"
        port = 587
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)

        recipients = data.to_dict("records")
        total = len(recipients)
        sent_count = 0
        logs = []

        for i, rec in enumerate(recipients, start=1):

            unit_name = rec.get("Unit Name", "Valued Mill")
            email = rec.get("Email")

            if pd.isna(email) or "@" not in email:
                continue

            msg = build_email(unit_name, sender_email, email)

            try:
                server.sendmail(sender_email, email, msg.as_string())
                sent_count += 1
                st.success(f"📨 Sent to {unit_name} ({email})")
                status = "Sent"
            except Exception as e:
                st.error(f"❌ Failed to {email}: {e}")
                status = "Failed"

            logs.append({
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Unit Name": unit_name,
                "Email": email,
                "Status": status
            })


            if i % BATCH_SIZE == 0:
                st.warning(f"⏸ Waiting {DELAY} seconds before next batch...")
                for remaining in range(DELAY, 0, -1):
                    timer_placeholder.info(f"⌛ Next batch in {remaining} seconds...")
                    time.sleep(1)
                    timer_placeholder.empty()

        server.quit()

        log_df = pd.DataFrame(logs)
        log_df.to_csv("sent_log.csv", index=False)

        st.success(f"🎉 Completed! {sent_count} emails sent.")
        st.info("📝 Log saved: sent_log.csv")

    st.markdown('</div>', unsafe_allow_html=True)
