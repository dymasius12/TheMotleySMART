#!/opt/anaconda3/envs/motley_smart/bin/python
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import yfinance as yf
import matplotlib.pyplot as plt

def get_stock_data(ticker):
    """Fetch stock data using yfinance."""
    stock = yf.Ticker(ticker)
    data = stock.history(period="1y")
    return data, stock

def display_stock_dashboard():
    """Display comprehensive stock info within the main application window."""
    ticker = stock_code_entry.get()
    if not ticker:
        messagebox.showerror("Error", "Please enter a stock code.")
        return
    
    try:
        _, stock = get_stock_data(ticker)
        info = stock.info

        # Set company name at the top center
        company_name_label.config(text=info['shortName'])

        # Formatting the information into categories

        # Left: General and Financial Info
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

        # Middle: Trading and Dividend Info
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

        # Right: Volume, Earnings, Balance Sheet, and Miscellaneous Info
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
        # Placeholder for future implementation
        messagebox.showinfo("Info", "This feature is not yet implemented.")
    elif choice == 3:  # Stock News
        # Placeholder for future implementation
        messagebox.showinfo("Info", "This feature is not yet implemented.")
    elif choice == 4:  # Exit Program
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
root.title("Stock Application")
root.geometry("800x500")
root.resizable(False, False)

# Style for a rounded button
style = ttk.Style()
style.configure('TButton', font=('Arial', 23), borderwidth='4')
style.map('TButton', background=[('active', 'cyan')])
button_height = 50  # or any other value you prefer
style.configure('TButton', padding=(0, button_height // 2, 0, button_height // 2))

# Landing Frame
landing_frame = tk.Frame(root)
landing_frame.pack(fill=tk.BOTH, expand=True)
logo_image = tk.PhotoImage(file="logo_mid.png")
logo_small_image = tk.PhotoImage(file="logo.png")
tk.Label(landing_frame, image=logo_image).pack(pady=20)
tk.Label(landing_frame, text="Stock Application", font=('Arial', 24)).pack(pady=20)
start_button = ttk.Button(landing_frame, text="Start", command=start_program, style='TButton', width=10) #Start Button
start_button.pack(pady=20)

# Menu Frame
menu_frame = tk.Frame(root)
back_button = tk.Button(menu_frame, text="←", command=go_back, fg="black", bg="blue", font=('Arial', 16), height=1, width=3)
back_button.pack(anchor="nw", padx=10, pady=10)
stock_code_entry = tk.Entry(menu_frame, font=('Arial', 16), width=30)
stock_code_entry.pack(pady=20)
menu_listbox = tk.Listbox(menu_frame, font=('Arial', 16), width=30, height=5)
menu_listbox.insert(1, "1. Stock Dashboard")
menu_listbox.insert(2, "2. Display Stock Price vs Time Graph")
menu_listbox.insert(3, "3. Stock Analysis on Stock Parameters")
menu_listbox.insert(4, "4. Stock News")
menu_listbox.insert(5, "5. Exit Program")
menu_listbox.pack(pady=20)
confirm_button = ttk.Button(menu_frame, text="Confirm", command=confirm_choice, style='TButton', width=10)
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
