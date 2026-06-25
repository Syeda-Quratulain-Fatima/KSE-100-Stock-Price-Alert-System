class Node:
    def __init__(self, stock, alert_type, threshold, actual_price, day):
        self.stock = stock
        self.alert_type = alert_type
        self.threshold = threshold
        self.actual_price = actual_price
        self.day = day
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.total_fired = 0

    def append(self, stock, alert_type, threshold, actual_price, day):
        new_node = Node(stock, alert_type, threshold, actual_price, day)
        if self.head is None:
            self.head = new_node
            self.total_fired += 1
            return None
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node
        self.total_fired += 1

    def traverse(self):
        if self.head is None:
            print("No alerts have fired yet")
            return None
        print("\n--- Full Alert Log (Chronological) ---")
        current = self.head
        count = 1
        while current is not None:
            print(f"  [{count}] Day {current.day} | {current.stock} | {current.alert_type} ALERT | Threshold: Rs.{current.threshold} | Actual: Rs.{current.actual_price}")
            current = current.next
            count += 1

    def traverse_by_stock(self, stock_name):
        if self.head is None:
            print("No alerts have fired yet")
            return None
        print(f"\n--- Alerts for {stock_name} ---")
        current = self.head
        found = 0
        while current is not None:
            if current.stock == stock_name:
                print(f"  Day {current.day} | {current.alert_type} ALERT | Threshold: Rs.{current.threshold} | Actual: Rs.{current.actual_price}")
                found += 1
            current = current.next
        if found == 0:
            print(f"  No alerts found for {stock_name}")
        return None