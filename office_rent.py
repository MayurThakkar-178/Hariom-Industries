import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ---- Page Config ----
st.set_page_config(page_title="Hariom Industries Email Tool", page_icon="📩", layout="centered")

st.title("📩 Hariom Industries - Email Tool")
st.write("Upload a CSV of agents/traders (with columns: `Name`, `Email`) to send emails directly.")

# ---- Sidebar for Credentials ----
st.sidebar.header("✉️ Email Account Settings")
sender_email = st.sidebar.text_input("Your Gmail Address", placeholder="youremail@gmail.com")
app_password = st.sidebar.text_input("App Password", type="password")

# ---- File Upload ----
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

# ---- Email Template ----
def generate_email(name):
    return f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family:Arial,Helvetica,sans-serif;background:#f4f6f8;padding:20px;">
      <div style="max-width:640px;margin:auto;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 12px rgba(0,0,0,0.1);">
        <img src="https://via.placeholder.com/1200x400.png?text=Hariom+Industries+Cotton+Exports" style="width:100%;display:block;">
        <div style="padding:24px;">
          <p>Dear {name},</p>
          <p>Greetings from <strong>Hariom Industries</strong>, a Gujarat-based cotton ginning company.  
          We specialize in <strong>Shankar-6 cotton bales</strong> and byproducts including cottonseed, cottonseed cake, lint waste, and seed oil.</p>
          <p>In addition to Shankar-6, we also process and supply <strong>Kalyan 797 cotton (variety 797)</strong>, ensuring diverse options to meet the specific needs of our buyers.</p>
          <div style="background:#fafafa;padding:16px;border-radius:8px;margin-top:16px;">
            <h3 style="margin:0 0 8px 0;">What we can supply</h3>
            <ul>
              <li>Shankar-6 Cotton Bales – contamination-controlled</li>
              <li>Kalyan 797 Cotton – widely used in local & export markets</li>
              <li>Cottonseed – suitable for oil extraction</li>
              <li>Cottonseed Cake – protein-rich cattle feed</li>
              <li>Lint / Cotton Waste – for open-end spinning & recycling</li>
            </ul>
          </div>
          <a href="mailto:hariomindustries5559@gmail.com?subject=Request%20for%20Cotton%20Specs%20and%20Prices&body=Hello%20Hariom%20Industries,%0D%0A%0D%0AI%20am%20interested%20in%20your%20cotton%20products.%20Please%20share%20detailed%20specifications%20and%20pricing.%0D%0A%0D%0AProducts%20Interested:%0D%0A[ ]%20Shankar-6%20Cotton%20Bales%0D%0A[ ]%20Kalyan%20797%20Cotton%0D%0A[ ]%20Cottonseed%0D%0A[ ]%20Cottonseed%20Cake%0D%0A[ ]%20Lint%20/%20Cotton%20Waste%0D%0A%0D%0ACompany%20Name:%20[Enter%20Here]%0D%0AContact%20Person:%20[Enter%20Here]%0D%0AContact%20Number:%20[Enter%20Here]%0D%0A%0D%0ARegards,%0D%0A" 
   style="display:inline-block;margin-top:20px;padding:12px 20px;background:#0b8457;color:#fff;border-radius:6px;text-decoration:none;">
   Request Specs & Prices
</a>

          <hr style="margin:24px 0;border:none;height:1px;background:#eee;">
          <p style="font-size:12px;color:#555;">Hariom Industries • Gujarat, India<br>
          📧 hariomindustries5559@gmail.com</p>
        </div>
      </div>
    </body>
    </html>
    """

# ---- Sending Emails ----
def send_email(to_email, subject, html_content):
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject

    # Attach HTML
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        return True
    except Exception as e:
        return str(e)

# ---- Main Logic ----
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success(f"CSV Loaded: {len(df)} contacts found ✅")
    st.dataframe(df.head())

    for idx, row in df.iterrows():
        name = row["Name"]
        email = row["Email"]
        st.markdown(f"### ✉️ Preview for **{name}** ({email})")
        st.components.v1.html(generate_email(name), height=600, scrolling=True)

    if sender_email and app_password:
        if st.button("🚀 Send Emails"):
            progress = st.progress(0)
            success_count = 0
            errors = []
            for i, row in df.iterrows():
                name, email = row["Name"], row["Email"]
                html_body = generate_email(name)
                result = send_email(email, "Cotton Products – Hariom Industries", html_body)
                if result is True:
                    success_count += 1
                else:
                    errors.append((email, result))
                progress.progress((i + 1) / len(df))
            st.success(f"✅ Sent {success_count} / {len(df)} emails successfully!")
            if errors:
                st.error("Some emails failed:")
                st.write(errors)
    else:
        st.warning("⚠️ Enter your Gmail and App Password in the sidebar to enable sending.")
