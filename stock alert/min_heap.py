class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, threshold, stock):
        new_node = (threshold, stock)
        self.heap.append(new_node)
        current = len(self.heap) - 1
        while current > 0:
            parent = (current - 1) // 2
            if self.heap[current][0] < self.heap[parent][0]:
                self.heap[current], self.heap[parent] = self.heap[parent], self.heap[current]
                current = parent
            else:
                break

    def extract_min(self):
        if len(self.heap) == 0:
            print("Min-Heap is empty")
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        current = 0
        while True:
            left = 2 * current + 1
            right = 2 * current + 2
            smallest = current
            if left < len(self.heap) and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right
            if smallest != current:
                self.heap[current], self.heap[smallest] = self.heap[smallest], self.heap[current]
                current = smallest
            else:
                break
        return root

    def peek(self):
        if len(self.heap) == 0:
            print("Min-Heap is empty")
            return None
        return self.heap[0]

    def display(self):
        if len(self.heap) == 0:
            print("No pending buy alerts")
            return None
        print("\n--- Pending Buy Alerts (Min-Heap) ---")
        current = 0
        while current < len(self.heap):
            print(f"  Stock: {self.heap[current][1]} | Threshold: Rs. {self.heap[current][0]}")
            current += 1

    def size(self):
        return len(self.heap)