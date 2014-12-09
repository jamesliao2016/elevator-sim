import copy

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def all(self):
        tmp = copy.deepcopy(self.items)
        x = []
        for i in range(0, len(tmp)):
            x.append([tmp.pop(), i])
        return x

    def get_next(self):
        tmp = copy.deepcopy(self.items)
        return tmp.pop()

    def remove(self, item):
        self.items.remove(item)

    def has(self, x):
        for item in self.items:
            if x == item:
                return True
        return False