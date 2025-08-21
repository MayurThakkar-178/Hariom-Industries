import streamlit as st
import pandas as pd
import yagmail

# ---- Page Config ----
st.set_page_config(page_title="Hariom Industries Email Sender", page_icon="📩", layout="centered")

st.title("📩 Hariom Industries - Bulk Email Sender")
st.write("Upload a CSV of agents/traders (with columns: `Name`, `Email`) and send branded emails directly.")

# ---- Gmail Login ----
st.sidebar.header("🔑 Gmail Login")
gmail_user = st.sidebar.text_input("Enter your Gmail address")
gmail_pass = st.sidebar.text_input("Enter your Gmail App Password", type="password")

# ---- File Upload ----
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

# ---- Email Generator ----
def generate_email(name):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Hariom Industries – Export Email</title>
      <style>
        body {{
          margin: 0;
          padding: 0;
          background: #f4f6f8;
          font-family: Arial, Helvetica, sans-serif;
        }}
        .container {{
          max-width: 640px;
          margin: 20px auto;
          background: #ffffff;
          border-radius: 16px;
          overflow: hidden;
          box-shadow: 0 6px 24px rgba(0,0,0,0.08);
        }}
        .banner img {{
          width: 100%;
          height: auto;
          display: block;
        }}
        .content {{
          padding: 28px;
        }}
        p {{
          margin: 8px 0;
          font-size: 15px;
          color: #555;
          line-height: 1.6;
        }}
        .card {{
          background: #fafafa;
          border: 1px solid #ececec;
          border-radius: 12px;
          padding: 16px 18px;
          margin-top: 20px;
        }}
        .card h3 {{
          margin: 0 0 8px 0;
          font-size: 18px;
          color: #222;
        }}
        .card ul {{
          margin: 8px 0;
          padding-left: 20px;
          font-size: 14px;
          color: #333;
        }}
        .btn {{
          display: inline-block;
          text-decoration: none;
          font-weight: 600;
          padding: 12px 18px;
          margin-top: 24px;
          border-radius: 8px;
          background: #0b8457;
          color: #ffffff;
        }}
        hr {{
          border: none;
          height: 1px;
          background: #eee;
          margin: 24px 0;
        }}
        .footer {{
          font-size: 12px;
          color: #777;
          padding: 0 28px 24px 28px;
          line-height: 1.5;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="banner">
          <img src="https://via.placeholder.com/1200x400.png?text=Hariom+Industries+Cotton+Exports" alt="Hariom Industries">
        </div>
        <div class="content">
          <p>
            Dear {name},
          </p>
          <p>
            Greetings from <strong>Hariom Industries</strong>, a Gujarat-based cotton ginning company.  
            We specialize in <strong>Shankar-6 cotton bales</strong> and byproducts including cottonseed, cottonseed cake, lint waste, and seed oil.
          </p>
          <p>
            In addition to Shankar-6, we also process and supply <strong>Kalyan 797 cotton (variety 797)</strong>, ensuring diverse options to meet the specific needs of our buyers.
          </p>
          <div class="card">
            <h3>What we can supply</h3>
            <ul>
              <li>Shankar-6 Cotton Bales – press-packed, contamination-controlled</li>
              <li>Kalyan 797 Cotton – widely used in local & export markets</li>
              <li>Cottonseed – suitable for oil extraction</li>
              <li>Cottonseed Cake – protein-rich cattle feed</li>
              <li>Lint / Cotton Waste – for open-end spinning & recycling</li>
            </ul>
          </div>
          <a href="mailto:hariomindustries5559@gmail.com?subject=Request%20for%20Cotton%20Specs%20and%20Prices&body=Hello%20Hariom%20Industries%2C%0D%0A%0D%0AI%20am%20interested%20in%20your%20cotton%20products.%20Please%20share%20detailed%20specifications%20and%20pricing.%0D%0A%0D%0ACompany%20Name%3A%20%5BEnter%20Here%5D%0D%0AContact%20Person%3A%20%5BEnter%20Here%5D%0D%0AContact%20Number%3A%20%5BEnter%20Here%5D%0D%0A%0D%0ARegards%2C" 
             class="btn">Request Specs & Prices</a>
          <hr>
          <div class="footer">
            Hariom Industries • Gujarat, India<br>
            hariomindustries5559@gmail.com
          </div>
        </div>
      </div>
    </body>
    </html>
    """

# ---- Send Emails ----
if uploaded_file and gmail_user and gmail_pass:
    df = pd.read_csv(uploaded_file)
    st.success(f"CSV Loaded: {len(df)} contacts found ✅")
    st.dataframe(df.head())

    if st.button("🚀 Send Emails Now"):
        try:
            yag = yagmail.SMTP(gmail_user, gmail_pass)
            sent_count = 0
            for _, row in df.iterrows():
                name = row["Name"]
                email = row["Email"]
                html_content = generate_email(name)
                yag.send(
                    to=email,
                    subject="High-Quality Cotton Bales & Byproducts from Hariom Industries",
                    contents=html_content,
                )
                sent_count += 1
            st.success(f"✅ Successfully sent {sent_count} emails!")
        except Exception as e:
            st.error(f"❌ Error: {e}")
else:
    st.info("👉 Please log in with Gmail and upload a CSV file to enable sending.")
