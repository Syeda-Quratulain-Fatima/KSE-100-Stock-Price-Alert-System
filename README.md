# KSE-100-Stock-Price-Alert-System

A Python-based real-time stock price monitoring and alert system
built on custom data structures — no heapq, no deque,
everything from scratch.

## What it does

Simulates 60 days of KSE-100 daily closing prices for 5 stocks.
Investors register buy/sell price threshold alerts. As prices
move, the system fires and permanently logs every triggered alert.

## Data Structures (all implemented from scratch)

---

| Structure          | Role                    | Key Complexity          |
| ------------------ | ----------------------- | ----------------------- |
| Min-Heap           | Buy alert registry      | Insert/Extract O(log n) |
| Max-Heap           | Sell alert registry     | Insert/Extract O(log n) |
| Singly Linked List | Chronological alert log | Append O(1)             |

---

## Key Finding

After running the full 60-day simulation, sell alerts fired
2.3x more than buy alerts — clustering in days 15–35 (bull phase).
Buy alerts fired in bursts around days 42–50 (pullback phase).
The system correctly tracked real KSE-100 market dynamics.

## Tech Stack

- Python
- Pandas (CSV loading only)
- Streamlit (frontend interface)

## Files

- alert_system.py — core program (Min-Heap, Max-Heap, SLL)
- stock_prices.csv — 60-day closing prices, 5 KSE-100 stocks
- app.py — Streamlit frontend

## Course

Data Structures and Algorithms (CSC211)
BSc Economics with Data Science — COMSATS University Islamabad
Spring 2026
