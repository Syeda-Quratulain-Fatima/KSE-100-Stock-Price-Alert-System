class MaxHeap:
    def __init__(self):
        self.heap = []

    def insert(self, threshold, stock):
        new_node = (threshold, stock)
        self.heap.append(new_node)
        current = len(self.heap) - 1
        while current > 0:
            parent = (current - 1) // 2
            if self.heap[current][0] > self.heap[parent][0]:
                self.heap[current], self.heap[parent] = self.heap[parent], self.heap[current]
                current = parent
            else:
                break

    def extract_max(self):
        if len(self.heap) == 0:
            print("Max-Heap is empty")
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        current = 0
        while True:
            left = 2 * current + 1
            right = 2 * current + 2
            largest = current
            if left < len(self.heap) and self.heap[left][0] > self.heap[largest][0]:
                largest = left
            if right < len(self.heap) and self.heap[right][0] > self.heap[largest][0]:
                largest = right
            if largest != current:
                self.heap[current], self.heap[largest] = self.heap[largest], self.heap[current]
                current = largest
            else:
                break
        return root

    def peek(self):
        if len(self.heap) == 0:
            print("Max-Heap is empty")
            return None
        return self.heap[0]

    def display(self):
        if len(self.heap) == 0:
            print("No pending sell alerts")
            return None
        print("\n--- Pending Sell Alerts (Max-Heap) ---")
        current = 0
        while current < len(self.heap):
            print(f"  Stock: {self.heap[current][1]} | Threshold: Rs. {self.heap[current][0]}")
            current += 1

    def size(self):
        return len(self.heap)