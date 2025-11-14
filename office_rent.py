import smtplib
import pandas as pd
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ---- Load CSV ----
# CSV must have columns: Unit Name, Email
data = pd.read_csv("cotton_mills.csv")

# ---- Gmail Credentials ----
sender_email = "Hariomindustries5559@gmail.com"
password = "your_app_password_here"  # Use Gmail App Password

# ---- SMTP Setup ----
smtp_server = "smtp.gmail.com"
port = 587

# ---- Email Body Template ----
def generate_email(unit_name):
    body = f"""
Subject: Introduction & Proposal for Cotton Supply Collaboration

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
    return body

# ---- Batching System ----
BATCH_SIZE = 50   # send 50 emails at a time
DELAY = 120       # wait 120 seconds between batches (adjust as needed)

# ---- Send Emails ----
server = smtplib.SMTP(smtp_server, port)
server.starttls()
server.login(sender_email, password)

recipients = data.to_dict("records")
sent_count = 0

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

    server.sendmail(sender_email, email, msg.as_string())
    sent_count += 1
    print(f"✅ Sent to {unit_name} ({email})")

    # batching pause
    if i % BATCH_SIZE == 0:
        print(f"⏸ Pausing for {DELAY} seconds after {BATCH_SIZE} emails...")
        time.sleep(DELAY)

server.quit()
print(f"🎉 Finished sending {sent_count} emails.")
