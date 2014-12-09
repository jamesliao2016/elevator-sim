import copy

class Queue:
    def __init__(self):
        self.items = []
        self.coordinates = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def all(self):
        # tmp = copy.deepcopy(self.items)
        # x = []
        # for i in range(0, len(tmp)):
        #     x.append([tmp.pop(), i])
        # return x
        return self.items

    def coordinate(self, x, y):
        if (x,y) not in list(self.coordinates):
            self.coordinates.insert(0,(x,y))

    def get_next_coordinate(self):
        return self.coordinates.pop()

    def get_coordinates(self):
        return self.coordinates

    def get_next(self):
        tmp = copy.deepcopy(self.items)
        return tmp.pop()

    def remove(self, item):
        self.items.remove(item)

    def rem_coordinate(self, x, y):
        if (x,y) in self.coordinates:
            self.coordinates.remove((x,y))

    def has(self, x):
        for item in self.items:
            if x == item:
                return True
        return False