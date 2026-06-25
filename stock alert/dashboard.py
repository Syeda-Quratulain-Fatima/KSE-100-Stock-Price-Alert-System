import streamlit as st
import pandas as pd
import sys
import os
import time

sys.path.insert(0, os.path.dirname(__file__))

from min_heap import MinHeap
from max_heap import MaxHeap
from linked_list import SinglyLinkedList

# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="KSE-100 Stock Alert System",
    page_icon="📈",
    layout="wide"
)

# ── Session State Init ────────────────────────────────────────
if "loaded" not in st.session_state:
    st.session_state.loaded = False
if "stock_data" not in st.session_state:
    st.session_state.stock_data = {}
if "stock_names" not in st.session_state:
    st.session_state.stock_names = []
if "current_day" not in st.session_state:
    st.session_state.current_day = 0
if "total_days" not in st.session_state:
    st.session_state.total_days = 0
if "buy_heaps" not in st.session_state:
    st.session_state.buy_heaps = {}
if "sell_heaps" not in st.session_state:
    st.session_state.sell_heaps = {}
if "alert_log" not in st.session_state:
    st.session_state.alert_log = SinglyLinkedList()
if "total_registered" not in st.session_state:
    st.session_state.total_registered = 0
if "tick_messages" not in st.session_state:
    st.session_state.tick_messages = []
if "demo_done" not in st.session_state:
    st.session_state.demo_done = False

# ── Helper Functions ──────────────────────────────────────────
def check_buy_alerts(stock, price, day):
    heap = st.session_state.buy_heaps[stock]
    while heap.size() > 0:
        top = heap.peek()
        if top is None:
            break
        if price <= top[0]:
            triggered = heap.extract_min()
            st.session_state.alert_log.append(stock, "BUY", triggered[0], price, day)
            st.session_state.tick_messages.append(
                f"BUY|🔴 BUY ALERT FIRED — {stock} dropped to Rs.{price} | Threshold was Rs.{triggered[0]} | Day {day}"
            )
        else:
            break

def check_sell_alerts(stock, price, day):
    heap = st.session_state.sell_heaps[stock]
    while heap.size() > 0:
        top = heap.peek()
        if top is None:
            break
        if price >= top[0]:
            triggered = heap.extract_max()
            st.session_state.alert_log.append(stock, "SELL", triggered[0], price, day)
            st.session_state.tick_messages.append(
                f"SELL|🟢 SELL ALERT FIRED — {stock} rose to Rs.{price} | Threshold was Rs.{triggered[0]} | Day {day}"
            )
        else:
            break

def run_one_tick():
    if not st.session_state.loaded:
        return "Please load data first"
    if st.session_state.current_day >= st.session_state.total_days:
        return "All 60 days simulated"
    st.session_state.tick_messages = []
    day_number = st.session_state.current_day + 1
    current = 0
    while current < len(st.session_state.stock_names):
        stock = st.session_state.stock_names[current]
        price = st.session_state.stock_data[stock][st.session_state.current_day]
        check_buy_alerts(stock, price, day_number)
        check_sell_alerts(stock, price, day_number)
        current += 1
    st.session_state.current_day += 1
    return "ok"

def run_all_ticks():
    if not st.session_state.loaded:
        return
    st.session_state.tick_messages = []
    while st.session_state.current_day < st.session_state.total_days:
        day_number = st.session_state.current_day + 1
        current = 0
        while current < len(st.session_state.stock_names):
            stock = st.session_state.stock_names[current]
            price = st.session_state.stock_data[stock][st.session_state.current_day]
            check_buy_alerts(stock, price, day_number)
            check_sell_alerts(stock, price, day_number)
            current += 1
        st.session_state.current_day += 1

def get_log_as_list():
    rows = []
    current = st.session_state.alert_log.head
    while current is not None:
        rows.append({
            "Day": current.day,
            "Stock": current.stock,
            "Alert Type": current.alert_type,
            "Threshold (Rs.)": current.threshold,
            "Actual Price (Rs.)": current.actual_price
        })
        current = current.next
    return rows

def get_buy_heap_contents():
    rows = []
    for stock in st.session_state.stock_names:
        heap = st.session_state.buy_heaps[stock]
        idx = 0
        while idx < len(heap.heap):
            rows.append({
                "Stock": stock,
                "Buy Threshold (Rs.)": heap.heap[idx][0],
                "Position in Heap": idx
            })
            idx += 1
    return rows

def get_sell_heap_contents():
    rows = []
    for stock in st.session_state.stock_names:
        heap = st.session_state.sell_heaps[stock]
        idx = 0
        while idx < len(heap.heap):
            rows.append({
                "Stock": stock,
                "Sell Threshold (Rs.)": heap.heap[idx][0],
                "Position in Heap": idx
            })
            idx += 1
    return rows

def load_csv():
    try:
        df = pd.read_csv("stock_prices.csv")
        names = list(df.columns[1:])
        st.session_state.stock_names = names
        st.session_state.total_days = len(df)
        st.session_state.current_day = 0
        for name in names:
            st.session_state.stock_data[name] = list(df[name])
            st.session_state.buy_heaps[name] = MinHeap()
            st.session_state.sell_heaps[name] = MaxHeap()
        st.session_state.alert_log = SinglyLinkedList()
        st.session_state.total_registered = 0
        st.session_state.tick_messages = []
        st.session_state.loaded = True
        return True
    except:
        return False

# ══════════════════════════════════════════════════════════════
# SIDEBAR — Navigation
# ══════════════════════════════════════════════════════════════
st.sidebar.title("📈 KSE-100 Alert System")
st.sidebar.caption("DSA Term Project | COMSATS")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home & Project Overview",
        "📂 Load Data",
        "🧠 How It Works (Flow)",
        "🔔 Register Alerts",
        "▶ Simulate Price Ticks",
        "📊 View Heaps",
        "📋 Alert Log (SLL)",
        "🎯 Demo Mode (Presentation)"
    ]
)

st.sidebar.divider()
if st.session_state.loaded:
    st.sidebar.success("✅ Data Loaded")
    st.sidebar.metric("Days Simulated", f"{st.session_state.current_day}/{st.session_state.total_days}")
    st.sidebar.metric("Alerts Fired", st.session_state.alert_log.total_fired)
else:
    st.sidebar.warning("⚠️ No data loaded yet")

# ══════════════════════════════════════════════════════════════
# PAGE 1 — Home & Project Overview
# ══════════════════════════════════════════════════════════════
if page == "🏠 Home & Project Overview":
    st.title("📈 KSE-100 Stock Price Alert System")
    st.subheader("CSC211 — Data Structures & Algorithms")
    st.caption("BS Economics with Data Science | COMSATS University Islamabad")
    st.divider()
    st.markdown("### 👩‍💻 Project Developer")

    st.markdown("""
        **Syeda Quratulain Fatima**  
""")
    st.divider()
    st.markdown("## What Problem Are We Solving?")
    st.info("""
    Investors in the KSE-100 market want to be notified automatically when a stock hits
    their target price — either to BUY when price drops low enough, or to SELL when price
    rises high enough. This system automates that entire process using three data structures
    built from scratch in Python.
    """)

    st.divider()
    st.markdown("## Project Architecture")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔴 Min-Heap")
        st.markdown("""
        **Used for: BUY Alerts**

        - Stores buy thresholds
        - Root = lowest threshold
        - When price FALLS below root → alert fires
        - Implemented from scratch
        - Operations: insert, extract-min, peek

        **Why Min-Heap?**
        The lowest buy threshold is always most at risk of firing when price drops. Min-Heap keeps it at the top automatically.
        """)

    with col2:
        st.markdown("### 🟢 Max-Heap")
        st.markdown("""
        **Used for: SELL Alerts**

        - Stores sell thresholds
        - Root = highest threshold
        - When price RISES above root → alert fires
        - Implemented from scratch
        - Operations: insert, extract-max, peek

        **Why Max-Heap?**
        The highest sell threshold is always most at risk of firing when price rises. Max-Heap keeps it at the top automatically.
        """)

    with col3:
        st.markdown("### 🔗 Singly Linked List")
        st.markdown("""
        **Used for: Alert Log**

        - Stores every fired alert
        - Appended in chronological order
        - Traversed front to back for display
        - Implemented from scratch
        - Operations: append, traverse, filter

        **Why SLL?**
        Alerts fire one by one and are only ever read in order. SLL append is O(1) and traversal is natural — no random access needed.
        """)

    st.divider()
    st.markdown("## Data")
    st.markdown("""
    - **5 KSE-100 stocks:** OGDC, HUBC, PSO, LUCK, ENGRO
    - **60 days** of simulated daily closing prices
    - Prices loaded from `stock_prices.csv` using pandas (only for loading — all processing done through custom data structures)
    """)

    st.divider()
    st.markdown("## File Structure")
    st.code("""
stock alert/
├── min_heap.py         ← MinHeap class (insert, extract_min, peek, display)
├── max_heap.py         ← MaxHeap class (insert, extract_max, peek, display)
├── linked_list.py      ← Node + SinglyLinkedList class (append, traverse)
├── stock_prices.csv    ← 60 days of prices for 5 stocks
├── alert_system.py     ← CLI menu (original required deliverable)
└── dashboard.py        ← This visual dashboard (Streamlit)
    """, language="")

# ══════════════════════════════════════════════════════════════
# PAGE 2 — Load Data
# ══════════════════════════════════════════════════════════════
elif page == "📂 Load Data":
    st.title("📂 Load Stock Price Data")
    st.markdown("This loads `stock_prices.csv` into memory and initializes one Min-Heap and one Max-Heap per stock.")
    st.divider()

    if st.button("📥 Load stock_prices.csv", use_container_width=True):
        success = load_csv()
        if success:
            st.success(f"✅ Loaded {st.session_state.total_days} days for: {', '.join(st.session_state.stock_names)}")
        else:
            st.error("❌ stock_prices.csv not found. Make sure it is in the same folder as dashboard.py")

    if st.session_state.loaded:
        st.divider()
        st.markdown("### Preview of Loaded Data")
        df = pd.read_csv("stock_prices.csv")
        st.dataframe(df, use_container_width=True)

        st.divider()
        st.markdown("### 60-Day Price Chart for All Stocks")
        df_chart = df.set_index("Day")
        st.line_chart(df_chart, use_container_width=True)

        st.divider()
        st.markdown("### Per-Stock Price Chart")
        selected = st.selectbox("Select a stock to zoom in", st.session_state.stock_names)
        st.line_chart(df[["Day", selected]].set_index("Day"), use_container_width=True)

# ══════════════════════════════════════════════════════════════
# PAGE 3 — How It Works (Flow)
# ══════════════════════════════════════════════════════════════
elif page == "🧠 How It Works (Flow)":
    st.title("🧠 How The System Works — Step by Step")
    st.divider()

    st.markdown("## The Complete Flow")

    st.markdown("### Step 1 — Load CSV")
    st.code("""
CSV File → pandas reads it → prices stored per stock in plain Python lists
           → one MinHeap created per stock  (for buy alerts)
           → one MaxHeap created per stock  (for sell alerts)
           → one SinglyLinkedList created   (shared alert log)
    """, language="")

    st.divider()
    st.markdown("### Step 2 — Register Alerts")
    st.code("""
User says: "Alert me if OGDC drops below Rs. 145"
→ MinHeap.insert((145, 'OGDC'))
→ Bubble Up: 145 moves to root if it's the smallest

User says: "Alert me if OGDC rises above Rs. 170"
→ MaxHeap.insert((170, 'OGDC'))
→ Bubble Up: 170 moves to root if it's the largest
    """, language="")

    st.divider()
    st.markdown("### Step 3 — Price Tick (One Day Passes)")
    st.code("""
Day 3 price of OGDC = Rs. 143

CHECK MIN-HEAP (buy alerts):
  Root = 145  →  Is 143 <= 145?  YES → BUY ALERT FIRES
  Extract 145 from heap (bubble down to restore order)
  Root = 140  →  Is 143 <= 140?  NO  → Stop

CHECK MAX-HEAP (sell alerts):
  Root = 170  →  Is 143 >= 170?  NO  → Stop

FIRED ALERT → appended to Singly Linked List:
  [OGDC | BUY | Threshold=145 | Actual=143 | Day=3] → None
    """, language="")

    st.divider()
    st.markdown("### Step 4 — Singly Linked List Grows")
    st.code("""
After Day 3:
Head → [OGDC|BUY|145|143|Day3] → None

After Day 7:
Head → [OGDC|BUY|145|143|Day3] → [HUBC|SELL|107|109|Day7] → None

After Day 10:
Head → [OGDC|BUY|145|143|Day3] → [HUBC|SELL|107|109|Day7] → [PSO|BUY|195|191|Day10] → None

Traversal = follow arrows from Head to None
    """, language="")

    st.divider()
    st.markdown("### Min-Heap Insert — Bubble Up Example")
    st.code("""
Insert 145, then 160, then 130 into MinHeap:

After inserting 145:        After inserting 160:        After inserting 130:
       145                         145                         130
                                  /                           /   \\
                                160                          145   160
                                                   (130 < 145 so it bubbles up to root)
    """, language="")

    st.divider()
    st.markdown("### Max-Heap Insert — Bubble Up Example")
    st.code("""
Insert 170, then 155, then 185 into MaxHeap:

After inserting 170:        After inserting 155:        After inserting 185:
       170                         170                         185
                                  /                           /   \\
                                155                          170   155
                                                   (185 > 170 so it bubbles up to root)
    """, language="")

    st.divider()
    st.markdown("### Why These Data Structures?")
    data = {
        "Data Structure": ["Min-Heap", "Max-Heap", "Singly Linked List"],
        "Used For": ["Buy Alerts", "Sell Alerts", "Alert Log"],
        "Insert Time": ["O(log n)", "O(log n)", "O(n) to tail / O(1) with tail pointer"],
        "Access Root": ["O(1)", "O(1)", "O(1) head"],
        "Extract": ["O(log n)", "O(log n)", "N/A"],
        "Why This One": [
            "Lowest buy threshold always at root — checked first when price falls",
            "Highest sell threshold always at root — checked first when price rises",
            "Append-only chronological log — no random access needed"
        ]
    }
    st.dataframe(pd.DataFrame(data), use_container_width=True)

# ══════════════════════════════════════════════════════════════
# PAGE 4 — Register Alerts
# ══════════════════════════════════════════════════════════════
elif page == "🔔 Register Alerts":
    st.title("🔔 Register Price Alerts")
    st.divider()

    if not st.session_state.loaded:
        st.warning("Please load data first from the Load Data page")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🔴 Register Buy Alert")
            st.caption("Alert fires when price DROPS BELOW your threshold")
            buy_stock = st.selectbox("Select Stock", st.session_state.stock_names, key="buy_stock")
            current_price_buy = st.session_state.stock_data[buy_stock][st.session_state.current_day] if st.session_state.current_day < st.session_state.total_days else "N/A"
            st.info(f"Current simulated price of {buy_stock}: Rs. {current_price_buy}")
            buy_threshold = st.number_input("Buy Threshold (Rs.)", min_value=0.0, step=0.5, key="buy_thresh")
            if st.button("✅ Register Buy Alert", use_container_width=True):
                st.session_state.buy_heaps[buy_stock].insert(buy_threshold, buy_stock)
                st.session_state.total_registered += 1
                st.success(f"Buy alert registered — {buy_stock} below Rs. {buy_threshold}")
                st.balloons()

        with col2:
            st.markdown("### 🟢 Register Sell Alert")
            st.caption("Alert fires when price RISES ABOVE your threshold")
            sell_stock = st.selectbox("Select Stock", st.session_state.stock_names, key="sell_stock")
            current_price_sell = st.session_state.stock_data[sell_stock][st.session_state.current_day] if st.session_state.current_day < st.session_state.total_days else "N/A"
            st.info(f"Current simulated price of {sell_stock}: Rs. {current_price_sell}")
            sell_threshold = st.number_input("Sell Threshold (Rs.)", min_value=0.0, step=0.5, key="sell_thresh")
            if st.button("✅ Register Sell Alert", use_container_width=True):
                st.session_state.sell_heaps[sell_stock].insert(sell_threshold, sell_stock)
                st.session_state.total_registered += 1
                st.success(f"Sell alert registered — {sell_stock} above Rs. {sell_threshold}")
                st.balloons()

        st.divider()
        st.markdown("### Currently Registered Alerts")
        col3, col4 = st.columns(2)
        with col3:
            buy_data = get_buy_heap_contents()
            if len(buy_data) == 0:
                st.info("No buy alerts registered yet")
            else:
                st.dataframe(pd.DataFrame(buy_data), use_container_width=True)
        with col4:
            sell_data = get_sell_heap_contents()
            if len(sell_data) == 0:
                st.info("No sell alerts registered yet")
            else:
                st.dataframe(pd.DataFrame(sell_data), use_container_width=True)

# ══════════════════════════════════════════════════════════════
# PAGE 5 — Simulate Price Ticks
# ══════════════════════════════════════════════════════════════
elif page == "▶ Simulate Price Ticks":
    st.title("▶ Simulate Price Ticks")
    st.caption("Each tick = one day passes. Prices are fed in. Both heaps are checked. Fired alerts go to SLL log.")
    st.divider()

    if not st.session_state.loaded:
        st.warning("Please load data first")
    else:
        st.progress(st.session_state.current_day / st.session_state.total_days)
        st.caption(f"Day {st.session_state.current_day} of {st.session_state.total_days} simulated")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("▶ Run One Day", use_container_width=True):
                result = run_one_tick()
                if result == "ok":
                    day = st.session_state.current_day
                    st.success(f"Day {day} simulated")
                    st.markdown("**Prices today:**")
                    current = 0
                    while current < len(st.session_state.stock_names):
                        stock = st.session_state.stock_names[current]
                        price = st.session_state.stock_data[stock][day - 1]
                        st.write(f"  {stock}: Rs. {price}")
                        current += 1
                    if len(st.session_state.tick_messages) == 0:
                        st.info("No alerts fired today")
                    for msg in st.session_state.tick_messages:
                        parts = msg.split("|", 1)
                        if parts[0] == "BUY":
                            st.error(parts[1])
                        else:
                            st.success(parts[1])
                else:
                    st.warning(result)

        with col2:
            if st.button("⏩ Run All Remaining Days", use_container_width=True):
                run_all_ticks()
                st.success(f"All {st.session_state.total_days} days simulated!")
                if len(st.session_state.tick_messages) == 0:
                    st.info("No alerts fired across remaining days")
                else:
                    st.markdown(f"**{len(st.session_state.tick_messages)} alerts fired:**")
                    for msg in st.session_state.tick_messages:
                        parts = msg.split("|", 1)
                        if parts[0] == "BUY":
                            st.error(parts[1])
                        else:
                            st.success(parts[1])

# ══════════════════════════════════════════════════════════════
# PAGE 6 — View Heaps
# ══════════════════════════════════════════════════════════════
elif page == "📊 View Heaps":
    st.title("📊 Heap Contents")
    st.caption("These are the alerts still waiting to fire. Once fired they move to the SLL log.")
    st.divider()

    tab1, tab2 = st.tabs(["🔴 Min-Heap (Buy Alerts)", "🟢 Max-Heap (Sell Alerts)"])

    with tab1:
        st.markdown("### Min-Heap — Buy Alert Thresholds")
        st.markdown("Root (position 0) = lowest threshold = most at risk when price falls")
        buy_data = get_buy_heap_contents()
        if len(buy_data) == 0:
            st.info("No pending buy alerts")
        else:
            df_buy = pd.DataFrame(buy_data)
            st.dataframe(df_buy, use_container_width=True)
            st.caption("Position 0 is the root of the heap — the lowest threshold")

    with tab2:
        st.markdown("### Max-Heap — Sell Alert Thresholds")
        st.markdown("Root (position 0) = highest threshold = most at risk when price rises")
        sell_data = get_sell_heap_contents()
        if len(sell_data) == 0:
            st.info("No pending sell alerts")
        else:
            df_sell = pd.DataFrame(sell_data)
            st.dataframe(df_sell, use_container_width=True)
            st.caption("Position 0 is the root of the heap — the highest threshold")

# ══════════════════════════════════════════════════════════════
# PAGE 7 — Alert Log (SLL)
# ══════════════════════════════════════════════════════════════
elif page == "📋 Alert Log (SLL)":
    st.title("📋 Alert Log — Singly Linked List Traversal")
    st.caption("Every fired alert is appended here in chronological order. This is a full SLL traversal from head to None.")
    st.divider()

    log_data = get_log_as_list()

    if len(log_data) == 0:
        st.info("No alerts have fired yet. Run some price ticks first.")
    else:
        st.markdown(f"### {len(log_data)} alerts in log")

        def color_rows(row):
            if row["Alert Type"] == "BUY":
                return ["background-color: #ffe6e6"] * len(row)
            else:
                return ["background-color: #e6ffe6"] * len(row)

        df_log = pd.DataFrame(log_data)
        st.dataframe(df_log.style.apply(color_rows, axis=1), use_container_width=True)

        st.divider()
        st.markdown("### Filter by Stock")
        if st.session_state.loaded:
            filter_stock = st.selectbox("Select Stock", st.session_state.stock_names)
            filtered = [row for row in log_data if row["Stock"] == filter_stock]
            if len(filtered) == 0:
                st.info(f"No alerts fired for {filter_stock}")
            else:
                st.dataframe(pd.DataFrame(filtered).style.apply(color_rows, axis=1), use_container_width=True)

        st.divider()
        st.markdown("### SLL Node Structure")
        st.code("""
class Node:
    def __init__(self, stock, alert_type, threshold, actual_price, day):
        self.stock        = stock         # e.g. "OGDC"
        self.alert_type   = alert_type    # "BUY" or "SELL"
        self.threshold    = threshold     # price that triggered alert
        self.actual_price = actual_price  # price on the day it fired
        self.day          = day           # which day it fired
        self.next         = None          # pointer to next node

# Traversal using required naming convention:
current = self.head
while current is not None:
    print(current.stock, current.alert_type)
    current = current.next
        """, language="python")

# ══════════════════════════════════════════════════════════════
# PAGE 8 — Demo Mode
# ══════════════════════════════════════════════════════════════
elif page == "🎯 Demo Mode (Presentation)":
    st.title("🎯 Demo Mode — Live Presentation Example")
    st.markdown("This page runs a pre-scripted realistic scenario for OGDC stock so you can explain the full flow to examiners clearly.")
    st.divider()

    st.markdown("## The Scenario We Will Demonstrate")
    st.info("""
    **Stock: OGDC (Oil & Gas Development Company)**

    - OGDC starts at Rs. 155 on Day 1
    - It gradually falls to Rs. 128 by Day 30
    - Then rises back up to Rs. 167 by Day 43

    We will register:
    - BUY alert at Rs. 145 → fires when price drops below 145
    - BUY alert at Rs. 135 → fires when price drops below 135
    - SELL alert at Rs. 160 → fires when price rises above 160

    Then simulate day by day and watch alerts fire automatically
    """)

    st.divider()
    st.markdown("## Step 1 — Load Data & Setup")

    if st.button("🚀 Run Full Demo Setup", use_container_width=True):
        success = load_csv()
        if not success:
            st.error("stock_prices.csv not found")
        else:
            st.session_state.buy_heaps["OGDC"].insert(145, "OGDC")
            st.session_state.total_registered += 1
            st.session_state.buy_heaps["OGDC"].insert(135, "OGDC")
            st.session_state.total_registered += 1
            st.session_state.sell_heaps["OGDC"].insert(160, "OGDC")
            st.session_state.total_registered += 1
            st.session_state.demo_done = True
            st.success("✅ Demo setup complete! 3 alerts registered for OGDC")

    if st.session_state.demo_done and st.session_state.loaded:
        st.divider()
        st.markdown("## Step 2 — What the Heaps Look Like Right Now")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🔴 Min-Heap (Buy Alerts)")
            st.code("""
Min-Heap internal array: [135, 145]

Tree view:
        135   ← ROOT (lowest = fires first when price drops)
       /
      145
            """)
            st.caption("135 is at root because it is the smallest — it will fire first if price keeps falling")

        with col2:
            st.markdown("### 🟢 Max-Heap (Sell Alerts)")
            st.code("""
Max-Heap internal array: [160]

Tree view:
        160   ← ROOT (only one alert registered)
            """)
            st.caption("160 will fire when OGDC rises above Rs. 160")

        st.divider()
        st.markdown("## Step 3 — Simulate Days One by One")
        st.markdown("Watch what happens as days pass. Click repeatedly to see alerts fire.")

        col3, col4 = st.columns(2)
        with col3:
            if st.button("▶ Simulate Next Day", use_container_width=True):
                result = run_one_tick()
                day = st.session_state.current_day
                if result == "ok":
                    ogdc_price = st.session_state.stock_data["OGDC"][day - 1]
                    st.markdown(f"### Day {day} — OGDC price: Rs. {ogdc_price}")

                    buy_root = st.session_state.buy_heaps["OGDC"].peek()
                    sell_root = st.session_state.sell_heaps["OGDC"].peek()

                    st.markdown("**Heap check:**")
                    if buy_root:
                        st.write(f"Min-Heap root (lowest buy threshold): Rs. {buy_root[0]}")
                        if ogdc_price <= buy_root[0]:
                            st.error(f"Rs.{ogdc_price} <= Rs.{buy_root[0]} → BUY ALERT FIRES!")
                        else:
                            st.write(f"Rs.{ogdc_price} > Rs.{buy_root[0]} → No buy alert today")
                    else:
                        st.write("Min-Heap is empty (all buy alerts fired)")

                    if sell_root:
                        st.write(f"Max-Heap root (highest sell threshold): Rs. {sell_root[0]}")
                        if ogdc_price >= sell_root[0]:
                            st.success(f"Rs.{ogdc_price} >= Rs.{sell_root[0]} → SELL ALERT FIRES!")
                        else:
                            st.write(f"Rs.{ogdc_price} < Rs.{sell_root[0]} → No sell alert today")
                    else:
                        st.write("Max-Heap is empty (all sell alerts fired)")

                    if len(st.session_state.tick_messages) > 0:
                        st.divider()
                        st.markdown("**Alerts fired this tick — appended to SLL:**")
                        for msg in st.session_state.tick_messages:
                            parts = msg.split("|", 1)
                            if parts[0] == "BUY":
                                st.error(parts[1])
                            else:
                                st.success(parts[1])
                else:
                    st.warning(result)

        with col4:
            st.markdown("### OGDC Price So Far")
            if st.session_state.current_day > 0:
                df = pd.read_csv("stock_prices.csv")
                df_ogdc = df[["Day", "OGDC"]].iloc[:st.session_state.current_day]
                st.line_chart(df_ogdc.set_index("Day"), use_container_width=True)

        st.divider()
        st.markdown("## Step 4 — SLL Alert Log So Far")
        log_data = get_log_as_list()
        ogdc_log = [row for row in log_data if row["Stock"] == "OGDC"]
        if len(ogdc_log) == 0:
            st.info("No OGDC alerts have fired yet — keep simulating days")
        else:
            st.markdown(f"**{len(ogdc_log)} OGDC alert(s) in the log:**")
            def color_rows(row):
                if row["Alert Type"] == "BUY":
                    return ["background-color: #ffe6e6"] * len(row)
                else:
                    return ["background-color: #e6ffe6"] * len(row)
            st.dataframe(pd.DataFrame(ogdc_log).style.apply(color_rows, axis=1), use_container_width=True)

            st.markdown("### SLL traversal happening here:")
            st.code("""
current = alert_log.head
while current is not None:
    if current.stock == "OGDC":
        print(current.day, current.alert_type, current.threshold, current.actual_price)
    current = current.next
            """, language="python")