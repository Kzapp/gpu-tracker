import requests
from bs4 import BeautifulSoup

MAX_PRICE = int(input("What is your max price?"))  # Change this to whatever your budget is

def check_gpu_stock():
    url = "https://www.newegg.com/p/pl?q=rtx&N=100007709"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Checking Newegg GPUs under ${MAX_PRICE}...\n")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("div", class_="item-cell")
        
        found = 0
        for item in items:
            name = item.find("a", class_="item-title")
            price = item.find("li", class_="price-current")
            
            if name and price:
                price_text = price.text.strip().replace(",", "").replace("–", "").strip()
                try:
                    price_num = float(price_text.replace("$", "").split()[0])
                    if price_num <= MAX_PRICE:
                        print(f"✅ {name.text.strip()}")
                        print(f"   💰 ${price_num}")
                        print("---")
                        found += 1
                except:
                    pass
        
        if found == 0:
            print(f"No GPUs found under ${MAX_PRICE}")
                
    except requests.exceptions.Timeout:
        print("Timed out")
    except Exception as e:
        print("Error:", e)

check_gpu_stock()