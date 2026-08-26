import os 
import smtplib
import logging
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

class GpuStock:

  def __init__(self, max_price: int) -> None:
    load_dotenv()
    self.max_price = max_price
    self.sender = os.environ.get("GMAIL_SENDER")
    self.receiver = os.environ.get("GMAIL_RECEIVER")
    self.password = os.environ.get("GMAIL_APP_PASSWORD")

  def send_email(self, subject:str, content:str) -> None:
      msg = MIMEText(content)
      msg["Subject"] = subject
      msg["From"] = self.sender
      msg["To"] = self.receiver

      with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
         server.login(self.sender, self.password)
         server.sendmail(self.sender, self.receiver, msg.as_string())


  def check_gpu_stock(self) -> None:
     url = "https://www.newegg.com/p/pl?q=rtx&N=100007709" 
     headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
     }
     try: 
        response = requests.get(url, headers=headers, timeout=10)
        logging.info("Connecting to URL - Success ")
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("div", class_="item-cell")
        
        for item in items:
           name = item.find("a", class_="item-title")
           link = item.find("a", class_="item-title")
           product_url = "https://www.newegg.com" + link["href"] if link else "No URL"
           price = item.find("li", class_="price-current")
           stock = item.find("p", class_="item-promo")
           stock_text = stock.text.strip() if stock else "In Stock"
           if name and price:
              price_text = price.text.strip().replace(",", "").replace("-", "").strip()
              try:
                 price_num = float(price_text.replace("$", "").split()[0])
                 if price_num <= self.max_price:
                    print(f"✅ {name.text.strip()}")
                    print(f"  💰 ${price_num}")
                    self.send_email("🎮 GPU ALERT!", f"{name.text.strip()}\nPrice: ${price_num}\nStock: {stock_text}\nLink: {product_url}")
                    logging.info("GPU(s) found - Email sent!")
              except ValueError as e:
                 logging.error(f"Value Error -->  {e}" )
                 print(f"Error: {e}")      
     except requests.exceptions.Timeout : 
        logging.error("Timeout Error - FAIL")
        print("The site took too long to respond")
     except requests.exceptions.ConnectionError :
        logging.error("Connection Error - FAIL")
        print("Connection failure could not reach the site")
     except requests.exceptions.RequestException :
        logging.error("Error - FAIL")
        print("We ran into an issue")
      