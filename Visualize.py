import tkinter as tk
from tkinter import ttk
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tabulate import tabulate

def get_stock_info(symbol):
    stock = yf.Ticker(symbol)
    company_name = stock.info.get('longName', 'N/A')
    current_price = stock.info.get('currentPrice', 'N/A')
    market_cap = stock.info.get('marketCap', 'N/A')
    dividend_yield = stock.info.get('dividendYield', 'N/A')
    earnings_per_share = stock.info.get('trailingEps', 'N/A')

    return {
        "Company Name": company_name + '\t',
        "Ticker Symbol": symbol,
        "Current Price": current_price,
        "Market Cap": market_cap,
        "Dividend Yield": dividend_yield,
        "Earnings Per Share": earnings_per_share
    }

def display_stock_info(stock_symbols):
    stock_info = {symbol: get_stock_info(symbol) for symbol in stock_symbols}

    headers = ['Company Name', 'Ticker Symbol', 'Current Price', 'Market Cap', 'Dividend Yield', 'Earnings Per Share']

    data = []
    for symbol, info in stock_info.items():
        data.append([info.get(key, 'N/A') for key in headers])

    formatted_data = ""
    for row in data:
        formatted_data += "\t".join(map(str, row)) + "\n"

    return formatted_data

def display_dividend_graphs(stock_symbols):
    plt.figure(figsize=(10, 6))
    for ticker_symbol in stock_symbols:
        ticker_data = yf.Ticker(ticker_symbol.strip())
        df = ticker_data.dividends
        if df.empty:
            continue

        data = df.resample('Y').sum()
        data = data.reset_index()
        data['Year'] = data['Date'].dt.year

        plt.plot(data['Year'], data['Dividends'], alpha=0.6, label=ticker_symbol)

    plt.title('Comparison of Dividends for Selected Ticker Symbols')
    plt.xlabel('Year')
    plt.ylabel('Dividends')
    plt.legend()
    plt.grid(True)

    return plt

def show_data():
    stocks = [symbol.strip() for symbol in entry.get().split(',')]

    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, display_stock_info(stocks))

    plt_dividend = display_dividend_graphs(stocks)
    plt_dividend.tight_layout()
    canvas = FigureCanvasTkAgg(plt_dividend.gcf(), master=frame_graph)
    canvas.draw()
    canvas.get_tk_widget().pack()

root = tk.Tk()
root.title('Stock Information and Dividend Comparison')

# Full screen settings
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.attributes('-fullscreen', True)
root.geometry(f"{screen_width}x{screen_height}")

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

frame_table = tk.Frame(notebook)
frame_graph = tk.Frame(notebook)

notebook.add(frame_table, text='Table')
notebook.add(frame_graph, text='Graph')

label = tk.Label(frame_table, text="Enter stock symbols separated by commas:")
label.grid(row=0, column=0)

entry = tk.Entry(frame_table)
entry.grid(row=0, column=1)

button = tk.Button(frame_table, text="Show Data", command=show_data)
button.grid(row=0, column=2)

text_output = tk.Text(frame_table, height=15, width=80)
text_output.grid(row=1, column=0, columnspan=3)

root.mainloop()
