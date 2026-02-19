# GPU Tracker Notes
This script scrapes Newegg's website by sending an HTTP request to their search page, reading the raw HTML response, and using BeautifulSoup to find and extract GPU names and prices from the page structure.
## What each part does

### Imports
We are calling in imports or Libraries that expand what Python can do. Features.
### send_email function

This function houses the email method to send an email to the user once a MAXPRICE is input along with data pulled from scraping/sending HTTP request. 
### check_gpu_stock function

This function uses Scrapres Neweggs website to pull data on GPU's. If there are no GPUS in the parameter (MAXPRICE) we update the user.
### Scheduling
Using the schedule import. We set the script to run every 60min, attached to automated emails that will be sent when the script finds GPU's.
By default the raw immediate data will be shared. However in a 60min increment another HTTP request is made to gather new data.