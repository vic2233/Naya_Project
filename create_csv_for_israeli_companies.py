import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from israeal_stocks import israel_stocks_list
from IPython import display

#my_ticker=yf.Ticker('PLTK')
#print(my_ticker.info['country'])
#stockinfo=my_ticker.info

#for key, value in stockinfo.items():
#    print(key,":",value)

# Read the CSV file and extract the first column
file_path = 'NASDAQ.csv'  # Replace with your actual CSV file path
df = pd.read_csv(file_path)

# Assuming the first column contains the NASDAQ symbols
nasdaq_symbols = df.iloc[:, 0]
#print(nasdaq_symbols)
# Use yfinance to get stock information and filter israelies companies
filtered_data = []

for symbol in nasdaq_symbols:
    stock = yf.Ticker(symbol)
    stock_info = stock.info
    
    # Check if the company is based in Israel
    if stock_info.get('country') == 'Israel':
        # Append relevant information to the list
        filtered_data.append({
            'Symbol': symbol ,
            'Company Name': stock_info.get('shortName'),
            'Current Price': stock_info.get('currentPrice')
        })
    print(symbol)

# Create a DataFrame from the filtered data and save it to a new CSV file
filtered_df = pd.DataFrame(filtered_data)
output_file_path = 'israeli_companies.csv' 
filtered_df.to_csv(output_file_path, index=False)

print(f"Filtered data saved to {output_file_path}")



