import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
#from israeal_stocks import israel_stocks_list

file_path = 'israeli_companies.csv' 
df = pd.read_csv(file_path)

# Assuming the first column contains the NASDAQ symbols
israel_stocks_list = df.iloc[:, 0]

# Define a function to generate the plot and save it as an image
def generate_plot(period_days,company):
    # Define the tickers
    nasdaq_ticker = '^IXIC'  # Nasdaq Composite Index
    israeli_tickers = israel_stocks_list
    #chosen_ticker='AUDC'
    chosen_ticker=company
    result = df.loc[df['Symbol'] == company, 'Company Name']
    # Define the time period
    start_date = pd.to_datetime('today') - pd.DateOffset(days=period_days)
    end_date = pd.to_datetime('today')

    # Fetch data
    nasdaq_data = yf.download(nasdaq_ticker, start=start_date, end=end_date)['Adj Close']
    chosen_data=yf.download(chosen_ticker, start=start_date, end=end_date)['Adj Close']
    
    israeli_data = {}
    for ticker in israeli_tickers:
        try:
            data = yf.download(ticker, start=start_date, end=end_date)['Adj Close']
            if not data.empty:
                israeli_data[ticker] = data
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")

    # Calculate percentage change
    if not nasdaq_data.empty:
        nasdaq_pct_change = nasdaq_data.pct_change().cumsum() * 100
    else:
        raise ValueError("No data available for Nasdaq Composite Index")
    
    if not chosen_data.empty:
        chosen_pct_change = chosen_data.pct_change().cumsum() * 100
        short_name = result.iloc[0]
    else:
        raise ValueError("No data available for Chosen ticker")
    
    # Calculate average percentage change for Israeli companies
    if israeli_data:
        israeli_df = pd.DataFrame(israeli_data)
        israeli_pct_change = israeli_df.pct_change().mean(axis=1).cumsum() * 100
    else:
        raise ValueError("No data available for Israeli companies")

    # Plotting graph
    plt.figure(figsize=(14, 7))

    # Plot Nasdaq
    plt.plot(nasdaq_pct_change.index, nasdaq_pct_change, label='Nasdaq Composite Index', color='blue')

    # Plot Chosen comp
    plt.plot(chosen_pct_change.index, chosen_pct_change, label=f'Chosen company :{short_name}', color='orange')

    # Plot Aggregated Israeli Companies
    plt.plot(israeli_pct_change.index, israeli_pct_change, label='Aggregated Israeli Companies', color='green')

    plt.xlabel('Date')
    plt.ylabel('Cumulative % Change')
    plt.title(f'Performance Comparison: Nasdaq Composite Index vs. Aggregated Israeli Companies ({period_days} days)')
    plt.legend()
    plt.grid(True)

    # Save the plot as an image
    plot_path = 'nasdaq_vs_israeli_companies.png'
    plt.savefig(plot_path)
    plt.close()  # Close the plot to avoid memory issues

    return plot_path


#generate_plot(30,'AUDC')
