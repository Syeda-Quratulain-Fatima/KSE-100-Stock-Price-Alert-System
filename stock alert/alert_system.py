import pandas as pd
from min_heap import MinHeap
from max_heap import MaxHeap
from linked_list import SinglyLinkedList

# ── Global State ──────────────────────────────────────────────
stock_data = {}
current_day = 0
total_days = 0
stock_names = []

buy_heaps = {}
sell_heaps = {}
alert_log = SinglyLinkedList()

total_registered = 0

# ── Load Data ─────────────────────────────────────────────────
def load_data():
    global stock_data, current_day, total_days, stock_names
    global buy_heaps, sell_heaps
    try:
        df = pd.read_csv("stock_prices.csv")
    except:
        print("Error: stock_prices.csv not found")
        return None
    stock_names = list(df.columns[1:])
    for name in stock_names:
        stock_data[name] = list(df[name])
        buy_heaps[name] = MinHeap()
        sell_heaps[name] = MaxHeap()
    total_days = len(df)
    current_day = 0
    print(f"\nLoaded {total_days} days of data for stocks: {', '.join(stock_names)}")

# ── Register Alerts ───────────────────────────────────────────
def register_buy_alert():
    global total_registered
    if len(stock_names) == 0:
        print("Please load data first")
        return None
    print(f"Available stocks: {', '.join(stock_names)}")
    stock = input("Enter stock name: ").strip().upper()
    if stock not in stock_names:
        print("Invalid stock name")
        return None
    threshold = input("Enter buy threshold price (Rs.): ").strip()
    if not threshold.replace('.','',1).isdigit():
        print("Invalid price entered")
        return None
    threshold = float(threshold)
    buy_heaps[stock].insert(threshold, stock)
    total_registered += 1
    print(f"Buy alert registered for {stock} at Rs. {threshold}")

def register_sell_alert():
    global total_registered
    if len(stock_names) == 0:
        print("Please load data first")
        return None
    print(f"Available stocks: {', '.join(stock_names)}")
    stock = input("Enter stock name: ").strip().upper()
    if stock not in stock_names:
        print("Invalid stock name")
        return None
    threshold = input("Enter sell threshold price (Rs.): ").strip()
    if not threshold.replace('.','',1).isdigit(): # .replace 
        print("Invalid price entered")
        return None
    threshold = float(threshold)
    sell_heaps[stock].insert(threshold, stock)
    total_registered += 1
    print(f"Sell alert registered for {stock} at Rs. {threshold}")

# ── Price Tick Logic ──────────────────────────────────────────
def run_tick():
    global current_day
    if len(stock_names) == 0:
        print("Please load data first")
        return None
    if current_day >= total_days:
        print("All 60 days have been simulated")
        return None
    day_number = current_day + 1
    print(f"\n--- Day {day_number} Prices ---")
    current = 0
    while current < len(stock_names):
        stock = stock_names[current]
        price = stock_data[stock][current_day]
        print(f"  {stock}: Rs. {price}")
        check_buy_alerts(stock, price, day_number)
        check_sell_alerts(stock, price, day_number)
        current += 1
    current_day += 1

def check_buy_alerts(stock, price, day):
    heap = buy_heaps[stock]
    while heap.size() > 0:
        top = heap.peek()
        if top is None:
            break
        if price <= top[0]:
            triggered = heap.extract_min()
            alert_log.append(stock, "BUY", triggered[0], price, day)
            print(f"  *** BUY ALERT FIRED: {stock} dropped to Rs.{price} (threshold Rs.{triggered[0]})")
        else:
            break

def check_sell_alerts(stock, price, day):
    heap = sell_heaps[stock]
    while heap.size() > 0:
        top = heap.peek()
        if top is None:
            break
        if price >= top[0]:
            triggered = heap.extract_max()
            alert_log.append(stock, "SELL", triggered[0], price, day)
            print(f"  *** SELL ALERT FIRED: {stock} rose to Rs.{price} (threshold Rs.{triggered[0]})")
        else:
            break

def run_all_ticks():
    if len(stock_names) == 0:
        print("Please load data first")
        return None
    if current_day >= total_days:
        print("All days already simulated")
        return None
    print(f"\nRunning all remaining {total_days - current_day} days...")
    while current_day < total_days:
        run_tick()

# ── View Functions ────────────────────────────────────────────
def view_buy_alerts():
    if len(stock_names) == 0:
        print("Please load data first")
        return None
    print("\n--- All Pending Buy Alerts ---")
    current = 0
    while current < len(stock_names):
        stock = stock_names[current]
        print(f"\n  {stock}:")
        buy_heaps[stock].display()
        current += 1

def view_sell_alerts():
    if len(stock_names) == 0:
        print("Please load data first")
        return None
    print("\n--- All Pending Sell Alerts ---")
    current = 0
    while current < len(stock_names):
        stock = stock_names[current]
        print(f"\n  {stock}:")
        sell_heaps[stock].display()
        current += 1

def view_full_log():
    alert_log.traverse()

def view_stock_alerts():
    if len(stock_names) == 0:
        print("Please load data first")
        return None
    print(f"Available stocks: {', '.join(stock_names)}")
    stock = input("Enter stock name: ").strip().upper()
    if stock not in stock_names:
        print("Invalid stock name")
        return None
    alert_log.traverse_by_stock(stock)

def view_summary():
    print("\n--- Summary ---")
    print(f"  Total alerts registered : {total_registered}")
    print(f"  Total alerts fired      : {alert_log.total_fired}")
    print(f"  Days simulated          : {current_day} / {total_days}")

# ── CLI Menu ──────────────────────────────────────────────────
def menu():
    while True:
        print("\n========================================")
        print("     STOCK PRICE ALERT SYSTEM")
        print("========================================")
        print("[1]  Load stock price data from CSV")
        print("[2]  Register a buy alert")
        print("[3]  Register a sell alert")
        print("[4]  Run one price tick (next day)")
        print("[5]  Run all remaining ticks")
        print("[6]  View pending buy alerts")
        print("[7]  View pending sell alerts")
        print("[8]  View full alert log")
        print("[9]  View alerts for a specific stock")
        print("[10] Summary")
        print("[0]  Exit")
        print("========================================")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            load_data()
        elif choice == "2":
            register_buy_alert()
        elif choice == "3":
            register_sell_alert()
        elif choice == "4":
            run_tick()
        elif choice == "5":
            run_all_ticks()
        elif choice == "6":
            view_buy_alerts()
        elif choice == "7":
            view_sell_alerts()
        elif choice == "8":
            view_full_log()
        elif choice == "9":
            view_stock_alerts()
        elif choice == "10":
            view_summary()
        elif choice == "0":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again")

if __name__ == "__main__":
    menu()