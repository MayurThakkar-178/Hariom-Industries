import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ---- Page Config ----
st.set_page_config(page_title="Hariom Industries Email Tool", page_icon="📩", layout="centered")

st.title("📩 Hariom Industries - Bulk Email Sender")
st.write("Upload a CSV with trader/agent emails (with column: `Email`) to send outreach emails.")

# ---- File Upload ----
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

# ---- Email Template (Generic) ----
def generate_email():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Hariom Industries – Cotton Exports</title>
      <style>
        body { font-family: Arial, sans-serif; background: #f4f6f8; padding: 20px; }
        .container { max-width: 640px; margin: auto; background: #fff; border-radius: 12px; padding: 24px; }
        h2 { color: #0b8457; }
        p { font-size: 15px; color: #333; line-height: 1.6; }
        ul { font-size: 15px; color: #444; }
        .footer { margin-top: 20px; font-size: 13px; color: #777; }
        a.btn {
            display: inline-block; margin-top: 20px;
            background: #0b8457; color: #fff; padding: 12px 18px;
            text-decoration: none; border-radius: 8px;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <h2>Greetings from Hariom Industries</h2>
        <p>
          We are a Gujarat-based cotton ginning company, specializing in <b>Shankar-6 cotton bales</b> 
          and byproducts including cottonseed, cottonseed cake, lint waste, and seed oil.
        </p>
        <p>
          In addition to Shankar-6, we also process and supply <b>Kalyan 797 cotton (variety 797)</b>, 
          ensuring diverse options to meet the specific needs of our buyers.
        </p>
        <p><b>Products Available:</b></p>
        <ul>
          <li>Shankar-6 Cotton Bales</li>
          <li>Kalyan 797 Cotton</li>
          <li>Cottonseed</li>
          <li>Cottonseed Cake</li>
          <li>Lint / Cotton Waste</li>
        </ul>
        <a href="mailto:hariomindustries5559@gmail.com?subject=Request%20for%20Cotton%20Specs%20and%20Prices&body=Hello%20Hariom%20Industries,%0D%0A%0D%0AI%20am%20interested%20in%20your%20cotton%20products.%20Please%20share%20detailed%20specifications%20and%20pricing.%0D%0A%0D%0AProducts%20Interested:%0D%0A[ ]%20Shankar-6%20Cotton%20Bales%0D%0A[ ]%20Kalyan%20797%20Cotton%0D%0A[ ]%20Cottonseed%0D%0A[ ]%20Cottonseed%20Cake%0D%0A[ ]%20Lint%20/%20Cotton%20Waste%0D%0A%0D%0ACompany%20Name:%20[Enter%20Here]%0D%0AContact%20Person:%20[Enter%20Here]%0D%0AContact%20Number:%20[Enter%20Here]%0D%0A%0D%0ARegards,%0D%0A" 
   style="display:inline-block;margin-top:20px;padding:12px 20px;background:#0b8457;color:#fff;border-radius:6px;text-decoration:none;">
   Request Specs & Prices
</a>
        <div class="footer">
          Hariom Industries • Gujarat, India<br>
          📩 hariomindustries5559@gmail.com
        </div>
      </div>
    </body>
    </html>
    """
    return html


# ---- Show Preview ----
if uploaded_file:
    st.subheader("📨 Email Preview (Generic)")
    st.components.v1.html(generate_email(), height=700, scrolling=True)

    # ---- Send Email Form ----
    sender_email = st.text_input("Enter your Gmail address")
    app_password = st.text_input("Enter your Gmail App Password", type="password")

    if st.button("📩 Send Emails"):
        try:
            df = pd.read_csv(uploaded_file)
            recipients = df["Email"].dropna().tolist()

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, app_password)

            for recipient in recipients:
                msg = MIMEMultipart("alternative")
                msg["From"] = sender_email
                msg["To"] = recipient
                msg["Subject"] = "Cotton Exports – Hariom Industries"
                msg.attach(MIMEText(generate_email(), "html"))

                server.sendmail(sender_email, recipient, msg.as_string())

            server.quit()
            st.success(f"✅ Emails sent successfully to {len(recipients)} contacts!")

        except Exception as e:
            st.error(f"❌ Error: {e}")
