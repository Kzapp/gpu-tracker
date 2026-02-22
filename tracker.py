# ── IMPORTS ──────────────────────────────────────────────
import requests          # Sends HTTP requests to websites (like a browser would)
import smtplib           # Handles sending emails via SMTP protocol
import schedule          # Lets us run functions on a timer (every hour)
import time              # Gives us time utilities like sleep()
from email.mime.text import MIMEText  # Formats our email message properly
from bs4 import BeautifulSoup         # Parses HTML so we can extract data from it

# ── USER INPUT ───────────────────────────────────────────
MAX_PRICE = int(input("What is your max price?"))  # Asks user for budget, converts string input to integer

# ── EMAIL FUNCTION ───────────────────────────────────────
def send_email(subject, body):
    sender = "kzapi47@gmail.com"       # Who the email is from
    receiver = "kzapi47@gmail.com"     # Who receives it (same account)
    password = "ocpmggurelouaczg"      # Gmail app password (not your real password)

    msg = MIMEText(body)               # Creates the email body as a text message
    msg["Subject"] = subject           # Sets the email subject line
    msg["From"] = sender               # Sets the sender field
    msg["To"] = receiver               # Sets the recipient field

    # Opens a secure SSL connection to Gmail's server on port 465
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)                    # Logs into Gmail
        server.sendmail(sender, receiver, msg.as_string()) # Sends the email

    print("Email Sent!")

# ── MAIN SCRAPING FUNCTION ───────────────────────────────
def check_gpu_stock():
    url = "https://www.newegg.com/p/pl?q=rtx&N=100007709"  # Newegg GPU search page URL
    
    # Fakes a real browser request so Newegg doesn't block us
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Checking Newegg GPUs under ${MAX_PRICE}...\n")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)  # Sends HTTP request, times out after 10 seconds
        soup = BeautifulSoup(response.text, "html.parser")          # Parses the raw HTML into something we can navigate
        items = soup.find_all("div", class_="item-cell")            # Finds every product card on the page (returns a list)
        
        found = 0  # Counter to track how many GPUs matched our budget
        
        for item in items:  # Loop through every product card
            name = item.find("a", class_="item-title")   # Grabs the product name element
            link = item.find("a", class_="item-title")   # Grabs the link element (same element as name)
            
            # Builds full product URL, or falls back to "No URL" if link not found
            url = "https://www.newegg.com" + link["href"] if link else "No URL"
            
            price = item.find("li", class_="price-current")  # Grabs the price element

            if name and price:  # Only proceed if both name and price exist
                # Cleans the price text by removing commas and dashes
                price_text = price.text.strip().replace(",", "").replace("–", "").strip()
                
                try:
                    # Converts price string to a float number (removes $ and takes first chunk)
                    price_num = float(price_text.replace("$", "").split()[0])
                    
                    if price_num <= MAX_PRICE:  # If price is within budget
                        print(f"✅ {name.text.strip()}")   # Print GPU name
                        print(f"   💰 ${price_num}")        # Print price
                        print("---")
                        # Send email alert with name, price, and direct link
                        send_email("🎮 GPU ALERT!", f"{name.text.strip()}\nPrice: ${price_num}\nLink: {url}")
                        found += 1  # Increment found counter
                        
                except Exception as e:
                    print("Error:", e)  # Print any parsing errors instead of silently failing
                    
        if found == 0:
            print(f"No GPUs found under ${MAX_PRICE}")  # Notify user if nothing matched
                
    except requests.exceptions.Timeout:
        print("Timed out")       # Handles case where Newegg takes too long to respond
    except Exception as e:
        print("Error:", e)       # Catches any other unexpected errors

# ── STARTUP MENU ─────────────────────────────────────────
print("\nHow would you like to run the tracker?")
print("1 - Run once and exit")
print("2 - Run every hour automatically")

choice = input("\nEnter 1 or 2: ").strip()

if choice == "1":
    # Runs once then exits cleanly back to terminal
    check_gpu_stock()
    print("\nDone. Exiting.")

elif choice == "2":
    # Schedules hourly runs and keeps script alive
    schedule.every(1).hour.do(check_gpu_stock)
    print("\nTracker running... checking every hour.")
    print("Press Ctrl+C to stop and return to terminal.\n")
    check_gpu_stock()  # Run immediately first
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
            print(".", end="", flush=True)
    except KeyboardInterrupt:
        # Catches Ctrl+C cleanly instead of showing an ugly error
        print("\n\nTracker stopped. Back to terminal.")

else:
    print("Invalid choice. Exiting.")