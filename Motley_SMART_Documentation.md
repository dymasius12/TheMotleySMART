
# The Motley S.M.A.R.T Stock Application Documentation

## Introduction

The Motley S.M.A.R.T is a stock application that enables users to view a dashboard containing comprehensive stock information, as well as a time series graph of stock prices. The app fetches data from the S&P 500 and provides an interactive GUI for user inputs and display.

## Prerequisites

- Python 3
- Libraries: tkinter, yfinance, matplotlib, pandas

## Code Structure

1. **Import Libraries**: The necessary libraries and modules are imported to support the GUI and fetch stock data.

2. **Data Retrieval**: 
    - `fetch_sp500_companies()`: Fetches a list of S&P 500 companies from Wikipedia.
  
3. **Utility Functions**:
    - `on_company_dropdown_select(event)`: Updates the stock ticker code in the input field based on the company name selected from the dropdown.
    - `get_stock_data(ticker)`: Uses `yfinance` to fetch stock data.
  
4. **Dashboard and Graph Display**:
    - `display_stock_dashboard()`: Displays a comprehensive dashboard of stock information.
    - `display_stock_price_vs_time()`: Plots a graph showing stock's closing prices over time.

5. **Main Menu and Control**:
    - `start_program()`: Transition from the landing page to the main menu.
    - `confirm_choice()`: Confirm the user's choice from the main menu and execute the corresponding action.
    - `exit_program()`: Exit the application.
    - `go_back()`: Navigate back to the previous frame.

6. **GUI Initialization**:
    - Configures the main window, frames, labels, buttons, dropdowns, and other GUI components.

7. **Main Loop Execution**:
    - The main loop of the tkinter application is executed with `root.mainloop()`.

## Usage

1. **Starting the Program**: When the program starts, the user is greeted with a landing page showcasing the application logo and a "Start" button.

2. **Main Menu**:
    - Users can either select a company name from the dropdown or manually input a stock code.
    - After selecting/inputting, users can choose from a menu of options to display the stock dashboard, visualize the stock price over time, or other functionalities.

3. **Stock Dashboard**: This dashboard provides a comprehensive view of the selected stock, including general, financial, trading, dividend, volume, earnings, balance sheet, and miscellaneous information.

4. **Stock Price vs Time**: This functionality displays a graph showing the stock's closing prices over a period of time.

5. **Navigation**: Users can navigate back and forth between the main menu and the stock dashboard.

---

This documentation provides a high-level overview of the application's structure and functionality. For more detailed insights or further customization, one should refer to the source code and comments therein.
