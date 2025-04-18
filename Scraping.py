import requests
from bs4 import BeautifulSoup
import pandas as pd
import h5py
import time
import os
import matplotlib.pyplot as plt
from datetime import datetime
import schedule
import csv


CONFIG_FILE = 'crypto_websites.csv'

def create_config_file():
    """Create a CSV configuration file if it doesn't exist"""
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Website', 'Description', 'URL', 'Target'])
            writer.writerow(['CoinMarketCap', 'Price of Bitcoin', 'https://coinmarketcap.com/currencies/bitcoin/', 'Bitcoin'])
            writer.writerow(['CoinMarketCap-ETH', 'Price of Ethereum', 'https://coinmarketcap.com/currencies/ethereum/', 'Ethereum'])
            writer.writerow(['CoinMarketCap-XRP', 'Price of XRP', 'https://coinmarketcap.com/currencies/xrp/', 'XRP']) # Xrp because I like it
        print(f"Created configuration file: {CONFIG_FILE}")


def read_config():
    """Read the configuration file"""
    if not os.path.exists(CONFIG_FILE):
        create_config_file()

    websites = []
    with open(CONFIG_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            websites.append(row)
    return websites
    

def scrape_coinmarketcap(target):
    """Scrape the price of a specific cryptocurrency from CoinMarketCap"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = f'https://coinmarketcap.com/currencies/bitcoin/'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            price_element = soup.select_one('.sc-65e7f566-0.WXGwg.base-text[data-test="text-cdp-price-display"]')
            price_text = price_element.text.strip().replace('$', '').replace(',', '') if price_element else "N/A"
            price = float(price_text) if price_text != "N/A" else 0
            return {'name': target, 'price': price}
        else:
            print(f"Failed to retrieve data from CoinMarketCap for {target}: Status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error scraping CoinMarketCap for {target}: {e}")
        return None


def scrape_coinmarketcap_ethereum(target):
    """Scrape the price of Ethereum from CoinMarketCap"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = 'https://coinmarketcap.com/currencies/ethereum/'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            price_element = soup.select_one('.sc-65e7f566-0.WXGwg.base-text[data-test="text-cdp-price-display"]')
            price_text = price_element.text.strip().replace('$', '').replace(',', '') if price_element else "N/A"
            price = float(price_text) if price_text != "N/A" else 0
            return {'name': target, 'price': price}
        else:
            print(f"Failed to retrieve Ethereum data from CoinMarketCap: Status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error scraping Ethereum from CoinMarketCap: {e}")
        return None
#This function was removed as I am only allowed a certain amount of scrapes per day for this page
#def scrape_alpha_vantage_stocks(target):
    #"""Scrape stock data from Alpha Vantage API"""
    # **TODO: Replace with your actual Alpha Vantage API key**
    #api_key = 'R8U65OLJSL53GV0Y'
    #url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={target}&apikey={api_key}'
    #try:
        #response = requests.get(url)
        #response.raise_for_status()
        #data = response.json()
        #print(f" API response for {target}:", data)
        #if 'Global Quote' in data and '05. price' in data['Global Quote']:
            #price = float(data['Global Quote']['05. price'])
            #return {'name': target, 'price': price}
        #else:
            #print(f"Could not retrieve price for {target} from Alpha Vantage API.")
            #return None
    #except requests.exceptions.RequestException as e:
        #print(f"Error fetching Alpha Vantage API for {target}: {e}")
        #return None
    #except Exception as e:
        #print(f"Error processing Alpha Vantage API response for {target}: {e}")
        #return None



#XRP scraping function
def scrape_coinmarketcap_xrp(target):
    """Scrape the price of XRP from CoinMarketCap"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = 'https://coinmarketcap.com/currencies/xrp/'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            price_element = soup.select_one('.sc-65e7f566-0.WXGwg.base-text[data-test="text-cdp-price-display"]')
            price_text = price_element.text.strip().replace('$', '').replace(',', '') if price_element else "N/A"
            price = float(price_text) if price_text != "N/A" else 0
            return {'name': target, 'price': price}
        else:
            print(f"Failed to retrieve XRP data from CoinMarketCap: Status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error scraping XRP from CoinMarketCap: {e}")
        return None



def scrape_all_sites():
    """Scrape data from all configured websites"""
    websites = read_config()

    for website in websites:
        print(f"Scraping {website['Website']} for {website['Target']}...")

        data = None
        if website['Website'] == 'CoinMarketCap' and website['Target'] == 'Bitcoin':
            data = scrape_coinmarketcap(website['Target'])
        elif website['Website'] == 'CoinMarketCap-ETH':
            data = scrape_coinmarketcap_ethereum(website['Target'])
        elif website['Website'] == 'CoinMarketCap-XRP':  
            data = scrape_coinmarketcap_xrp(website['Target'])
        else:
            print(f"No scraper implemented for {website['Website']}")
            continue

        if data:
            save_to_hdf5(data, website['Website'])
        else:
            print(f"No data scraped from {website['Website']} for {website['Target']}")

    # Create visualizations after scraping
    create_time_series_visualizations()




def save_to_hdf5(data, source):
    """Save the scraped data to the HDF5 file"""
    if data:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file_path = f'crypto_data/crypto_prices.h5'
        with h5py.File(file_path, 'a') as f:
            group_name = f"{source}_{timestamp.replace(' ', '_').replace(':', '-')}"
            if group_name not in f:
                group = f.create_group(group_name)
            else:
                group = f[group_name]
            dataset_name = data['name'].replace(' ', '_').replace('-', '_')
            if dataset_name not in group:
                dset = group.create_dataset(dataset_name, data=data['price'])
            else:
                dset = group[dataset_name]
                dset[...] = data['price']
            dset.attrs['name'] = data['name']
            dset.attrs['price'] = data['price']
            dset.attrs['timestamp'] = timestamp
        print(f"Data saved to {file_path} under group {group_name} for {data['name']}")


# In[745]:


def create_time_series_visualizations():
   """Create visualizations of cryptocurrency/stock price trends by source"""
   file_path = 'crypto_data/crypto_prices.h5'

   if not os.path.exists(file_path):
       print("No data available for visualization yet.")
       return

   source_data = {}

   with h5py.File(file_path, 'r') as f:
       for group_name in f.keys():
           group = f[group_name]
           source = group_name.split('_')[0]  

           for crypto_name in group.keys():
               if isinstance(group[crypto_name], h5py.Dataset):
                   dataset = group[crypto_name]
                   if 'price' in dataset.attrs and 'timestamp' in dataset.attrs:
                       price = dataset[()]
                       timestamp_str = dataset.attrs['timestamp']
                       crypto_name_for_key = dataset.attrs['name'].replace(' ', '_').replace('-', '_') 
                       key = f"{crypto_name_for_key}_{source}" 

                       if key not in source_data:
                           source_data[key] = {'timestamps': [], 'prices': []}
                       source_data[key]['timestamps'].append(timestamp_str)
                       source_data[key]['prices'].append(price)
                   else:
                       print(f"Warning: Dataset '{crypto_name}' in group '{group_name}' is missing 'price' or 'timestamp'.")

   if not os.path.exists('visualizations'):
       os.makedirs('visualizations')

   for key, data in source_data.items():
       if len(data['timestamps']) > 1:
           plt.figure(figsize=(12, 6))
           timestamps = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in data['timestamps']]

           plt.plot(timestamps, data['prices'], marker='o', linestyle='-')

           plt.title(f"{key.replace('_', ' ')} Price Over Time")
           plt.xlabel('Timestamp')
           plt.ylabel('Price (USD)')
           plt.grid(True)
           plt.xticks(rotation=45)
           plt.tight_layout()

           plot_path = f"visualizations/{key}_time_series.png"
           plt.savefig(plot_path)
           plt.close()

           print(f"💪 Created visualization: {plot_path}")


# In[746]:


def scrape_all_sites():
    """Scrape data from all configured websites"""
    websites = read_config()

    for website in websites:
        print(f"Scraping {website['Website']} for {website['Target']}...")

        data = None
        if website['Website'] == 'CoinMarketCap' and website['Target'] == 'Bitcoin':
            data = scrape_coinmarketcap(website['Target'])
        elif website['Website'] == 'CoinMarketCap-ETH':
            data = scrape_coinmarketcap_ethereum(website['Target'])
        elif website['Website'] == 'CoinMarketCap-XRP':  
            data = scrape_coinmarketcap_xrp(website['Target'])
        else:
            print(f"No scraper implemented for {website['Website']}")
            continue

        if data:
            save_to_hdf5(data, website['Website'])
        else:
            print(f"No data scraped from {website['Website']} for {website['Target']}")

    # Create visualizations after scraping
    create_time_series_visualizations()


# In[747]:


def run_daily_job():
    """Run the scraping job once and schedule it for daily execution"""
    print(f"Starting cryptocurrency price scraping at {datetime.now()}")
    scrape_all_sites()
    
    # Schedule the job to run daily
    schedule.every().day.at("12:00").do(scrape_all_sites)
    
    print("Scheduled to run daily at 12:00. Keep the script running to execute scheduled jobs.")
    print("Press Ctrl+C to exit.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  
    except KeyboardInterrupt:
        print("Script terminated by user.")


# In[748]:


def run_scheduled_job():
    """Runs the scraping job."""
    print(f"Running cryptocurrency price scraping at {datetime.now()}")
    scrape_all_sites()


# In[749]:


if __name__ == "__main__":
    # Create config file if it doesn't exist
    create_config_file()

    # Run one scrape immediately (optional)
    print("Running initial scrape...")
    run_scheduled_job()

    # Schedule to run once a day at 12:00 PM
    #schedule.every().day.at("12:00").do(run_scheduled_job)
    schedule.every(1).hours.do(run_scheduled_job) # For testing and efficiency

    print("Scheduled to run daily at 12:00 PM. Keep the script running.")
    print("Press Ctrl+C to exit.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Script terminated by user.")










#schedule.clear() 


# In[ ]:




