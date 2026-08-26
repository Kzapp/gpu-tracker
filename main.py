from gpu_script import GpuStock
import schedule
import time

price = int(input("Enter max price for GPU search:\n"))

gpu = GpuStock(price)



while True: 
    print("#1 - Checks Neweggs site live")
    print("#2 - Checks Neweggs site scheduled for every hour")
    print("#3 - Exits the script")
    choice = input("\nSelect option (1,2 or 3) ").strip()
    
    if choice == "1":
      gpu.check_gpu_stock()
    elif choice == "2":
      schedule.every(1).hour.do(gpu.check_gpu_stock)
      gpu.check_gpu_stock()
      while True:
          schedule.run_pending()
          time.sleep(60)
    elif choice == "3":
       print("Goodbye!")
       break

