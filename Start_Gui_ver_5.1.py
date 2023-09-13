#!/opt/anaconda3/envs/motley_smart/bin/python
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
from newsapi import NewsApiClient
from config import API_KEY
import datetime

# Fetching S&P 500 Companies Using pandas_datareader
def fetch_sp500_companies():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url, header=0)
    sp500_companies = tables[0]
    return sp500_companies

sp500_companies_df = fetch_sp500_companies()
company_name_to_ticker = dict(zip(sp500_companies_df['Security'], sp500_companies_df['Symbol']))

def on_company_dropdown_select(event):
    """Update the stock_code_entry with the ticker when a company is selected from the dropdown."""
    # Get the selected company or industry
    selected_value = company_dropdown.get()
    
    # If the selected value is a company (not an industry), update the entry field with its ticker
    ticker = company_name_to_ticker.get(selected_value)
    if ticker:
        stock_code_entry.delete(0, tk.END)
        stock_code_entry.insert(0, ticker)

def get_stock_data(ticker):
    """Fetch stock data using yfinance."""
    stock = yf.Ticker(ticker)
    data = stock.history(period="1y")
    return data, stock

def display_stock_dashboard():
    """Display comprehensive stock info within the main application window."""
    input_value = stock_code_entry.get()
    if not input_value:
        messagebox.showerror("Error", "Please enter a stock code or company name.")
        return

    # Check if input is a company name, and if so, get the corresponding ticker
    ticker = company_name_to_ticker.get(input_value, input_value)
    
    try:
        data, stock = get_stock_data(ticker)
        info = stock.info

        # Set company name at the top center
        company_name_label.config(text=info['shortName'])

        # Formatting the information into categories
        general_info = (
            f"Name: {info['shortName']}\n"
            f"Sector: {info.get('sector', 'N/A')}\n"
            f"Industry: {info.get('industry', 'N/A')}\n"
            f"Country: {info.get('country', 'N/A')}\n"
            f"Website: {info.get('website', 'N/A')}\n\n"
        )
        financial_info = (
            f"Market Cap: {info.get('marketCap', 'N/A')}\n"
            f"Forward P/E: {info.get('forwardPE', 'N/A')}\n"
            f"Price-to-Book: {info.get('priceToBook', 'N/A')}\n"
            f"Trailing EPS: {info.get('trailingEps', 'N/A')}\n\n"
        )
        trading_info = (
            f"52 Week High: {info['fiftyTwoWeekHigh']}\n"
            f"52 Week Low: {info['fiftyTwoWeekLow']}\n"
            f"50 Day Average: {info.get('fiftyDayAverage', 'N/A')}\n"
            f"200 Day Average: {info.get('twoHundredDayAverage', 'N/A')}\n\n"
        )
        dividend_info = (
            f"Dividend Rate: {info.get('dividendRate', 'N/A')}\n"
            f"Dividend Yield: {info.get('dividendYield', 'N/A')}\n"
            f"Ex-Dividend Date: {info.get('exDividendDate', 'N/A')}\n\n"
        )
        volume_info = (
            f"Average Volume: {info.get('averageVolume', 'N/A')}\n"
            f"Volume: {info.get('volume', 'N/A')}\n"
            f"Last Volume: {info.get('lastVolume', 'N/A')}\n\n"
        )
        earnings_info = (
            f"Earnings Quarterly Growth: {info.get('earningsQuarterlyGrowth', 'N/A')}\n"
            f"Trailing Annual Dividend Rate: {info.get('trailingAnnualDividendRate', 'N/A')}\n\n"
        )
        balance_sheet_info = (
            f"Total Cash: {info.get('totalCash', 'N/A')}\n"
            f"Total Debt: {info.get('totalDebt', 'N/A')}\n"
            f"Quick Ratio: {info.get('quickRatio', 'N/A')}\n"
            f"Current Ratio: {info.get('currentRatio', 'N/A')}\n\n"
        )
        miscellaneous_info = (
            f"Beta: {info.get('beta', 'N/A')}\n"
            f"Book Value: {info.get('bookValue', 'N/A')}\n"
            f"Currency: {info.get('currency', 'N/A')}\n"
            f"Is ESG Populated: {info.get('isEsgPopulated', 'N/A')}\n"
        )

        # Update labels with fetched data
        general_info_label.config(text=general_info)
        financial_info_label.config(text=financial_info)
        trading_info_label.config(text=trading_info)
        dividend_info_label.config(text=dividend_info)
        volume_info_label.config(text=volume_info)
        earnings_info_label.config(text=earnings_info)
        balance_sheet_info_label.config(text=balance_sheet_info)
        miscellaneous_info_label.config(text=miscellaneous_info)

        # Hide the menu_frame and show the dashboard_frame
        menu_frame.pack_forget()
        dashboard_frame.pack(fill=tk.BOTH, expand=True)
        
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching data for {ticker}: {str(e)}")

def fetch_news_articles(company_name, api_key):
    newsapi = NewsApiClient(api_key=api_key)
    today = datetime.date.today()
    thirty_days_ago = today - datetime.timedelta(days=30)
    str_thirty_days_ago = thirty_days_ago.strftime('%Y-%m-%d')
    str_today = today.strftime('%Y-%m-%d')
    top_headlines = newsapi.get_everything(q=company_name,
                                           from_param=str_thirty_days_ago,
                                           to=str_today,
                                           language='en',
                                           sort_by='publishedAt',
                                           page_size=5)
    return top_headlines['articles']

def display_news_window():
    # Fetch the selected company's name from the dropdown
    company_name = company_dropdown.get()
    
    # If no company is selected, show an error and return
    if not company_name:
        tk.messagebox.showwarning("Warning", "Please select a company first.")
        return

    # Fetch the news articles for the selected company
    articles = fetch_news_articles(company_name, API_KEY)
    
    # Create a new tkinter window for displaying news
    news_window = tk.Toplevel()
    news_window.title(f"Stock News for {company_name}")
    news_window.geometry("800x600")  # Set window size (width x height)
    
    # Create a scrollable Text widget to display the articles
    news_text = tk.Text(news_window, wrap=tk.WORD, height=20, width=80)
    scrollbar = tk.Scrollbar(news_window, command=news_text.yview)
    news_text.configure(yscrollcommand=scrollbar.set)
    
    # Pack the Text widget and Scrollbar into the window
    news_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Insert the fetched articles into the Text widget
    for article in articles:
        news_text.insert(tk.END, "TITLE: " + article['title'] + "\n")
        news_text.insert(tk.END, "DESCRIPTION: " + article['description'] + "\n")
        news_text.insert(tk.END, "URL: " + article['url'] + "\n")
        news_text.insert(tk.END, "PUBLISHED AT: " + article['publishedAt'] + "\n")
        news_text.insert(tk.END, "-" * 50 + "\n\n")


def display_stock_price_vs_time():
    """Display stock's closing prices vs time graph."""
    ticker = stock_code_entry.get()
    if not ticker:
        messagebox.showerror("Error", "Please enter a stock code.")
        return
    
    try:
        data, _ = get_stock_data(ticker)
        data['Close'].plot(title=f"{ticker} Stock Price vs Time")
        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.grid(True)
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching data for {ticker}: {str(e)}")

def analyze_stock_parameters(stock_info):
    """
    Enhanced analysis function to provide more descriptive results.
    """
    analysis_results = {
        'Profitability': ('❌ No', 'RoE is less than 12%'),
        'Stability': ('❌ No', 'Beta is out of the range 0.8 to 1.3'),
        'Credibility': ('❌ No', 'Debt ratio is less than or equal to 0.8')
    }
    
    # Profitability Analysis
    roe = stock_info.get('returnOnEquity', 0)
    if roe >= 0.12:
        analysis_results['Profitability'] = ('✅ Yes', f'RoE is {roe*100:.2f}%')
    
    # Stability Analysis
    beta = stock_info.get('beta', 0)
    if 0.8 < beta < 1.3:
        analysis_results['Stability'] = ('✅ Yes', f'Beta is {beta:.2f}')
    
    # Credibility Analysis
    total_debt = stock_info.get('totalDebt', 0)
    total_assets = stock_info.get('totalAssets', 0)
    debt_ratio = 0
    if total_assets != 0:
        debt_ratio = total_debt / total_assets
    if debt_ratio > 0.8:
        analysis_results['Credibility'] = ('✅ Yes', f'Debt ratio is {debt_ratio:.2f}')
    
    return analysis_results

def display_stock_analysis():
    """Display the enhanced stock analysis results in a new window."""
    input_value = stock_code_entry.get()
    if not input_value:
        messagebox.showerror("Error", "Please enter a stock code or company name.")
        return
    ticker = company_name_to_ticker.get(input_value, input_value)
    _, stock = get_stock_data(ticker)
    info = stock.info

    # Analyze the stock
    analysis_results = analyze_stock_parameters(info)

    # Create a new window to display the results
    analysis_window = tk.Toplevel(root)
    analysis_window.title("Stock Analysis Results")

    # Display the results in labels
    for i, (parameter, (result, description)) in enumerate(analysis_results.items()):
        color = "green" if "✅" in result else "red"
        tk.Label(analysis_window, text=f"{parameter}: {result}", font=('Arial', 12), fg=color).grid(row=2*i, column=0, padx=10, pady=5)
        tk.Label(analysis_window, text=f"{description}", font=('Arial', 10), fg=color).grid(row=2*i+1, column=0, padx=10, pady=5)

    analysis_window.mainloop()

def monte_carlo_simulation(ticker, num_simulations=1000, num_days=252):
    """Run a Monte Carlo simulation for future stock prices."""
    
    # Fetch historical data
    data, _ = get_stock_data(ticker)
    
    # Calculate daily returns
    returns = data['Close'].pct_change().dropna()
    
    # Calculate mean and standard deviation of daily returns
    mu = returns.mean()
    sigma = returns.std()
    
    # Initialize array for simulations
    simulations = np.zeros((num_days, num_simulations))
    
    # Set first row of simulations to the last closing price
    simulations[0] = data['Close'].iloc[-1]
    
    # Simulate future stock prices
    for simulation in range(num_simulations):
        for day in range(1, num_days):
            simulations[day, simulation] = (simulations[day - 1, simulation]
                                            * (1 + np.random.normal(mu, sigma)))
    
    # Compute the average path
    average_path = np.mean(simulations, axis=1)
    
    return simulations, average_path

def display_monte_carlo_simulation():
    """Display the results of the Monte Carlo simulation."""
    
    ticker = stock_code_entry.get()
    if not ticker:
        messagebox.showerror("Error", "Please enter a stock code.")
        return
    
    try:
        simulations, average_path = monte_carlo_simulation(ticker)
        
        # Compute the 2.5th and 97.5th percentiles
        upper_bound = np.percentile(simulations, 95, axis=1)
        lower_bound = np.percentile(simulations, 5, axis=1)
        
        plt.figure(figsize=(10,5))
        for i in range(simulations.shape[1]):
            plt.plot(simulations[:, i], color='gray', alpha=0.1)
        
        # Plot the average path in blue
        plt.plot(average_path, color='blue', label='Average Path')
            
        # Plot the upper and lower bounds of the 90% confidence interval
        plt.plot(upper_bound, color='red', label='95th Percentile')
        plt.plot(lower_bound, color='red', label='5th Percentile')
            
        plt.title(f"{ticker} Monte Carlo Simulation of Stock Prices with 90% Confidence Interval")
        plt.xlabel("Days")
        plt.ylabel("Simulated Stock Price")
        plt.legend()
        plt.grid(True)
        plt.show()
        
    except Exception as e:
        messagebox.showerror("Error", f"Error running Monte Carlo simulation for {ticker}: {str(e)}")

def start_program():
    landing_frame.pack_forget()
    menu_frame.pack(fill=tk.BOTH, expand=True)
    stock_code_entry.pack(pady=20)
    menu_listbox.pack(pady=20)
    confirm_button.pack(pady=20)

def confirm_choice():
    choice = menu_listbox.curselection()[0]
    if choice == 0:  # Stock Dashboard
        display_stock_dashboard()
    elif choice == 1:  # Display Stock Price vs Time Graph
        display_stock_price_vs_time()
    elif choice == 2:  # Stock Analysis on Stock Parameters
        display_stock_analysis()
    elif choice == 3:  # Stock News
        #For news button
        display_news_window()  # Adjust the layout as per your design
    elif choice == 4:  # Monte Carlo Simulation
        display_monte_carlo_simulation()
    elif choice == 5:  # Exit Program
        exit_program()

def exit_program():
    root.destroy()

def go_back():
    if dashboard_frame.winfo_ismapped():
        # If we're in the dashboard frame, go back to the main menu
        dashboard_frame.pack_forget()
        menu_frame.pack(fill=tk.BOTH, expand=True)
    elif menu_frame.winfo_ismapped():
        # If we're in the main menu, go back to the landing page
        menu_frame.pack_forget()
        landing_frame.pack(fill=tk.BOTH, expand=True)

# Main window
root = tk.Tk()
root.title("The Motley S.M.A.R.T")
root.geometry("800x500")
root.resizable(False, False)

# Style for a rounded button
style = ttk.Style()
style.configure('TButton', font=('Arial', 23), borderwidth='4')
style.map('TButton', background=[('active', 'cyan')])
button_height = 25  # or any other value you prefer
style.configure('TButton', padding=(0, button_height // 2, 0, button_height // 2))

# Landing Frame
landing_frame = tk.Frame(root)
landing_frame.pack(fill=tk.BOTH, expand=True)
logo_image = tk.PhotoImage(file="logo_mid.png")  # Ensure you have this image in the same directory or provide the full path
logo_small_image = tk.PhotoImage(file="logo.png")  # Ensure you have this image in the same directory or provide the full path
tk.Label(landing_frame, image=logo_image).pack(pady=20)
tk.Label(landing_frame, text="Stock Application", font=('Arial', 24)).pack(pady=20)
start_button = ttk.Button(landing_frame, text="Start", command=start_program, style='TButton', width=10) #Start Button
start_button.pack(pady=20)

# Menu Frame
menu_frame = tk.Frame(root)

# Back button
back_button = tk.Button(menu_frame, text="←", command=go_back, fg="black", bg="blue", font=('Arial', 16), height=1, width=3)
back_button.pack(anchor="nw", padx=10, pady=10)

# Label for company dropdown
tk.Label(menu_frame, text="Please choose the company name from the dropdown below:", font=('Arial', 18)).pack(pady=2)

# Group by industries and create a list of companies for each industry with formatting
industry_to_companies = {}
formatted_dropdown_values = []
for industry, group in sp500_companies_df.groupby('GICS Sector'):
    industry_to_companies[industry] = group['Security'].tolist()
    formatted_dropdown_values.append(f"--{industry} Industry--")
    formatted_dropdown_values.extend(group['Security'].tolist())

# Create the dropdown for company names
company_dropdown = ttk.Combobox(menu_frame, values=formatted_dropdown_values, font=('Arial', 16), width=30)
company_dropdown.pack(pady=10)

# Bind the dropdown select event
company_dropdown.bind("<<ComboboxSelected>>", on_company_dropdown_select)

# Label for stock code entry
tk.Label(menu_frame, text="OR please input the stock code below:", font=('Arial', 18)).pack(pady=2)

# Stock code entry
stock_code_entry = tk.Entry(menu_frame, font=('Arial', 16), width=30)
stock_code_entry.pack(pady=10)

# Label and Listbox for menu options
tk.Label(menu_frame, text="Choose the Menu Option Below:", font=('Arial', 18)).pack(pady=2)
menu_listbox = tk.Listbox(menu_frame, font=('Arial', 16), width=30, height=5)
menu_listbox.insert(1, "1. Stock Dashboard")
menu_listbox.insert(2, "2. Display Stock Price vs Time Graph")
menu_listbox.insert(3, "3. Stock Analysis on Stock Parameters")
menu_listbox.insert(4, "4. Stock News")
menu_listbox.insert(5, "5. Monte Carlo Simulation of Stock Prices")
menu_listbox.insert(6, "6. Exit Program")
menu_listbox.pack(pady=10)

# Search button
confirm_button = ttk.Button(menu_frame, text="Search Stock", command=confirm_choice, style='TButton', width=15)
confirm_button.pack(pady=20)

# Dashboard Frame
dashboard_frame = tk.Frame(root)
dashboard_back_button = tk.Button(dashboard_frame, text="←", command=go_back, fg="black", bg="blue", font=('Arial', 14), height=1, width=3)
dashboard_back_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

company_name_label = tk.Label(dashboard_frame, font=('Arial', 18, 'bold'))
company_name_label.grid(row=0, column=1, sticky="n", padx=10, pady=10)

logo_label = tk.Label(dashboard_frame, image=logo_small_image)
logo_label.grid(row=6, column=2, sticky="se", padx=0, pady=3)

# LEFT SIDE
# General Info
tk.Label(dashboard_frame, text="General Info", font=('Arial', 12, 'bold')).grid(row=1, column=0, sticky="nw", padx=10, pady=10)
general_info_label = tk.Label(dashboard_frame, font=('Arial', 12), justify=tk.LEFT)
general_info_label.grid(row=2, column=0, sticky="nw", padx=10, pady=10)

# Financial Info
tk.Label(dashboard_frame, text="Financial Info", font=('Arial', 12, 'bold')).grid(row=3, column=0, sticky="nw", padx=10, pady=10)
financial_info_label = tk.Label(dashboard_frame, font=('Arial', 12), justify=tk.LEFT)
financial_info_label.grid(row=4, column=0, sticky="nw", padx=10, pady=10)

# Balance Sheet Info
tk.Label(dashboard_frame, text="Balance Sheet Info", font=('Arial', 12, 'bold')).grid(row=5, column=0, sticky="nw", padx=10, pady=10)
balance_sheet_info_label = tk.Label(dashboard_frame, font=('Arial', 12), justify=tk.LEFT)
balance_sheet_info_label.grid(row=6, column=0, sticky="nw", padx=10, pady=10)

# MIDDLE
# Trading Info
tk.Label(dashboard_frame, text="Trading Info", font=('Arial', 12, 'bold')).grid(row=1, column=1, sticky="nw", padx=10, pady=10)
trading_info_label = tk.Label(dashboard_frame, font=('Arial', 12), justify=tk.LEFT)
trading_info_label.grid(row=2, column=1, sticky="nw", padx=10, pady=10)

# Dividend Info
tk.Label(dashboard_frame, text="Dividend Info", font=('Arial', 12, 'bold')).grid(row=3, column=1, sticky="nw", padx=10, pady=10)
dividend_info_label = tk.Label(dashboard_frame, font=('Arial', 12), justify=tk.LEFT)
dividend_info_label.grid(row=4, column=1, sticky="nw", padx=10, pady=10)

# Miscellaneous Info
tk.Label(dashboard_frame, text="Miscellaneous Info", font=('Arial', 12, 'bold')).grid(row=5, column=1, sticky="nw", padx=10, pady=10)
miscellaneous_info_label = tk.Label(dashboard_frame, font=('Arial', 12), justify=tk.LEFT)
miscellaneous_info_label.grid(row=6, column=1, sticky="nw", padx=10, pady=10)

# RIGHT SIDE
# Volume Info
tk.Label(dashboard_frame, text="Volume Info", font=('Arial', 12, 'bold')).grid(row=1, column=2, sticky="nw", padx=10, pady=10)
volume_info_label = tk.Label(dashboard_frame, font=('Arial', 12), justify=tk.LEFT)
volume_info_label.grid(row=2, column=2, sticky="nw", padx=10, pady=10)

# Earnings Info
tk.Label(dashboard_frame, text="Earnings Info", font=('Arial', 12, 'bold')).grid(row=3, column=2, sticky="nw", padx=10, pady=10)
earnings_info_label = tk.Label(dashboard_frame, font=('Arial', 12), justify=tk.LEFT)
earnings_info_label.grid(row=4, column=2, sticky="nw", padx=10, pady=10)

root.mainloop()

