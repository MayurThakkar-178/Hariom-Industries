import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ---- Page Config ----
st.set_page_config(page_title="Hariom Industries Email Tool", page_icon="📩", layout="centered")

st.title("📩 Hariom Industries - Bulk Email Sender")
st.write("Upload a CSV with columns: `Email`, `Name`, `Company` to send personalized outreach emails.")

# ---- Email Template (Personalized) ----
def generate_email(name=None, company=None):
    greeting = "Hello"
    if name and company:
        greeting = f"Hello {name} from {company},"
    elif name:
        greeting = f"Hello {name},"
    elif company:
        greeting = f"Hello team at {company},"

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Hariom Industries – Cotton Exports</title>
      <style>
        body {{ font-family: Arial, sans-serif; background: #f4f6f8; padding: 20px; }}
        .container {{ max-width: 640px; margin: auto; background: #fff; border-radius: 12px; padding: 24px; }}
        h2 {{ color: #0b8457; }}
        p {{ font-size: 15px; color: #333; line-height: 1.6; }}
        ul {{ font-size: 15px; color: #444; }}
        .footer {{ margin-top: 20px; font-size: 13px; color: #777; }}
        .btn {{
            display: inline-block; margin-top: 20px;
            background: #0b8457; color: #fff; padding: 12px 18px;
            text-decoration: none; border-radius: 8px;
        }}
        strong {{ color: #0b8457; }}
      </style>
    </head>
    <body>
      <div class="container">
        <h2>Greetings from Hariom Industries</h2>
        <p>{greeting}</p>
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
        <p>
          We would be glad to connect further to discuss details about cotton exports, 
          and would love to work with you.
        </p>
        <p><strong>
        This email is purely for business inquiry purposes and is sent in accordance with the IT Act, 2000. This is not spam.
        </strong></p>

        <!-- Request Specs & Prices Button -->
        <a href="mailto:hariomindustries5559@gmail.com?subject=Request%20for%20Cotton%20Specs%20and%20Prices&body=Hello%20Hariom%20Industries,%0D%0A%0D%0AI%20am%20interested%20in%20your%20cotton%20products.%20Please%20share%20detailed%20specifications%20and%20pricing.%0D%0A%0D%0ACompany%20Name:%20[Enter%20Here]%0D%0AContact%20Person:%20[Enter%20Here]%0D%0AContact%20Number:%20[Enter%20Here]%0D%0A%0D%0AProducts%20Interested:%20[Tick%20from%20list]%0D%0A%0D%0ARegards," 
        class="btn">Request Specs & Prices</a>

        <div class="footer">
          Hariom Industries • Gujarat, India<br>
          📩 hariomindustries5559@gmail.com
        </div>
      </div>
    </body>
    </html>
    """
    return html

# ---- File Upload ----
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

# ---- Show Preview ----
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📨 Email Preview (Generic Example)")
    st.components.v1.html(generate_email("John", "ABC Textiles"), height=700, scrolling=True)

    # ---- Send Email Form ----
    sender_email = st.text_input("Enter your Gmail address")
    app_password = st.text_input("Enter your Gmail App Password", type="password")

    if st.button("📩 Send Personalized Emails"):
        try:
            recipients = df.to_dict("records")

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, app_password)

            sent_count = 0
            for rec in recipients:
                email = rec.get("Email")
                name = rec.get("Name")
                company = rec.get("Company")

                if pd.isna(email):
                    continue

                msg = MIMEMultipart("alternative")
                msg["From"] = sender_email
                msg["To"] = email
                msg["Subject"] = "Cotton Exports – Hariom Industries"
                msg.attach(MIMEText(generate_email(name, company), "html"))

                server.sendmail(sender_email, email, msg.as_string())
                sent_count += 1

            server.quit()
            st.success(f"✅ Personalized emails sent successfully to {sent_count} contacts!")

        except Exception as e:
            st.error(f"❌ Error: {e}")

